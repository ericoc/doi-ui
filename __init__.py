import logging
from flask import (
    Flask, flash, render_template, make_response, request, send_from_directory
)
from flask_caching import Cache
from datetime import date, datetime
from doi import DOI

# Flask.
app = Flask(__name__)
app.config.from_pyfile("config.py")
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
            # Check cache for the DOI information
            cache_key = get_doi.replace("/", "_")
            in_cache = cache.get(cache_key)
            if in_cache:
                _doi = in_cache
                cached = True
            else:
                _doi = DOI(get_doi)
                cache.set(cache_key, _doi)

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


# Create a template filter function for Jinja2 to display timestamps.
@app.template_filter()
def prettytime(when: (date, datetime, str, None) = None):

    # Format date and datetime, as needed.
    if when:
        date_fmt = ""
        if type(when) == date:
            date_fmt = "%A, %B %d, %Y"
        if type(when) == datetime:
            date_fmt = "%A, %B %d, %Y @ %H:%M:%S %z (%Z)"

        if date_fmt:
            when = when.strftime(date_fmt)

    return when
