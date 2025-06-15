import logging
from flask import (
    Flask, flash, render_template, make_response, request, send_from_directory
)
from flask_caching import Cache
from doi import DOI
from prettytime import prettytime
from orcid import PublicAPI


# Flask.
app = Flask(__name__)
app.config.from_pyfile("config.py")
app.add_template_filter(prettytime)
cache = Cache(app)

# Logging.
logger = logging.getLogger(__name__)
LOG_LEVEL = logging.ERROR
if (
    app.config.get("DEBUG") or app.config.get("TESTING") or
    app.config.get("ENV", "") in ("development", "dev")
):
    LOG_LEVEL = logging.DEBUG
logging.basicConfig(
    datefmt="%Y-%m-%d %H:%M:%S %Z",
    format="%(asctime)s [%(levelname)s] (%(process)d): %(message)s",
    handlers=(logging.StreamHandler(),),
    level=LOG_LEVEL
)

# Main (Jinja2) template to search DOI.
@app.route("/")
def index():
    _doi = None
    cached: bool = False
    code: int = 200
    err_msg: (str, None) = None
    get_doi: (str, None) = request.args.get("doi")

    # Gather information about submitted DOI ("?doi=" GET parameter).
    if get_doi:
        try:
            # Check cache for DOI information.
            doi_cache_key = get_doi.replace("/", "_")
            in_cache = cache.get(doi_cache_key)
            if in_cache:
                _doi = in_cache
                cached = True
            else:
                _doi = DOI(get_doi)
                cache.set(doi_cache_key, _doi)

        # Handle any errors that may occur.
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

        if _doi and _doi.authors:
            orcid_api = PublicAPI(
                institution_key=app.config["ORCID_API_CLIENT_ID"],
                institution_secret=app.config["ORCID_API_CLIENT_SECRET"]
            )
            orcid_token = orcid_api.get_search_token_from_orcid()
            base_url = "https://orcid.org/"
            uni = "University of Pennsylvania"

            for _author in _doi.authors:
                if _author.orcid and _author.is_penn_affiliated is False:
                    short_orcid = _author.orcid.replace(base_url, "")
                    employments = orcid_api.read_record_public(
                        orcid_id=short_orcid,
                        request_type="employments",
                        token=orcid_token
                    )
                    if employments:
                        employ_summary = employments.get("employment-summary")
                        for employment in employ_summary:
                                employ_org = employment.get("organization")
                                if employ_org:
                                    employ_org_name = employ_org.get("name")
                                    if employ_org_name == uni:
                                        _author.is_penn_affiliated = True

        # Display any error message that was generated.
        if err_msg:
            flash(err_msg)

    # Return template response, with header whether DOI was found in cache.
    resp = make_response(
        render_template("index.html.j2", doi=_doi),
        code
    )
    resp.headers["X-DOI-Cached"] = cached
    return resp


@app.route("/static/<path:path>")
def statics(path):
    # Static content.
    return send_from_directory("static", path)
