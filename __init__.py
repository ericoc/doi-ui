import logging
from flask import (
    Flask, flash, render_template, make_response, request, send_from_directory
)
from .DOI import DOI

# Flask.
app = Flask(__name__)
app.config.from_pyfile("config.py")

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

@app.route("/")
def index():
    # Return (Jinja2) template with DOI details.
    code = 200
    doi = None
    get_doi = request.args.get("doi")

    if get_doi:
        try:
            doi = DOI(get_doi)
            logger.debug(vars(doi))
        except Exception as exc:
            code = 404
            logger.exception(exc)
            flash(message=str(exc))
    return make_response(render_template("index.html.j2", doi=doi), code)


@app.route('/static/<path:path>')
def statics(path):
    # Static content.
    return send_from_directory("static", path)
