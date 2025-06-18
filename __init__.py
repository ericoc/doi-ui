import logging
from flask import Flask, \
    flash, render_template, make_response, request, send_from_directory
from flask_caching import Cache
from doi import DOI
from prettytime import prettytime
from orcid import PublicAPI


# Flask.
app = Flask(__name__)
app.config.from_pyfile("config.py")
app.add_template_filter(prettytime)
cache = Cache(app)
debug = app.config.get("DEBUG", False)

# Logging.
logger = logging.getLogger(__name__)
logging.basicConfig(
    datefmt="%Y-%m-%d %H:%M:%S %Z",
    format="%(asctime)s [%(levelname)s] (%(process)d): %(message)s",
    handlers=(logging.StreamHandler(),),
    level=logging.DEBUG if debug else logging.INFO
)

# Main (Jinja2) template to search DOI.
@app.route("/")
def index():
    _doi: (None, DOI) = None
    code: int = 200
    err_msg: str = ""

    # Handle submitted DOI ("?doi=" GET parameter).
    get_doi: str = request.args.get("doi", "")
    if get_doi:

        # Check cache for DOI information.
        doi_cache_key = get_doi.replace("/", "_")
        doi_in_cache = cache.get(doi_cache_key)

        # Use cached DOI information, if it was found.
        if doi_in_cache:
            _doi = doi_in_cache

        # Otherwise, try to gather DOI information, and cache it.
        else:

            try:
                _doi = DOI(get_doi)
                cache.set(doi_cache_key, _doi)

            # Handle any exceptions.
            except ValueError:
                code = 400
                err_msg = "Invalid DOI format!"
            except FileNotFoundError:
                code = 404
                err_msg = "No such DOI was found!"
            except Exception as exc:
                code = 500
                logger.exception(exc)
                err_msg = str(exc)

        # Authors.
        if _doi and _doi.authors:

            # Connect to ORCID.org public API, and get a search token.
            orcid_api = PublicAPI(
                institution_key=app.config["ORCID_API_CLIENT_ID"],
                institution_secret=app.config["ORCID_API_CLIENT_SECRET"]
            )
            orcid_token = orcid_api.get_search_token_from_orcid()

            # Iterate each DOI author ORCID to see if they are Penn-affiliated.
            for author in _doi.authors:

                # Search ORCID, if author is not already affiliated with Penn.
                if author.orcid and author.is_penn is False:
                    orcid_id = author.orcid.replace("https://orcid.org/", "")

                    # Use ORCID employments from cache, if found.
                    orcid_in_cache = cache.get(orcid_id)
                    if orcid_in_cache:
                        employments = orcid_in_cache

                    # Otherwise, gather and cache ORCID employments.
                    else:
                        employments = orcid_api.read_record_public(
                            orcid_id=orcid_id,
                            request_type="employments",
                            token=orcid_token
                        )
                        cache.set(orcid_id, employments)

                    # Check each employment for "University of Pennsylvania".
                    if employments:
                        employ_summary = employments.get("employment-summary")
                        for employment in employ_summary:
                            employ_org = employment.get("organization")
                            if employ_org:
                                org_name = employ_org.get("name")
                                if org_name == "University of Pennsylvania":
                                    author.is_penn = True
                                    _doi.is_penn = True

        # Display any error message that was generated.
        if err_msg:
            flash(err_msg)

    return make_response(
        render_template(
            template_name_or_list="index.html.j2",
            debug=debug,
            doi=_doi
        ), code
    )


@app.route("/static/<path:path>")
def statics(path):
    # Static content.
    return send_from_directory("static", path)
