import logging
from flask import (
    Flask, flash, render_template, make_response, request, send_from_directory
)
from DOI import DOI

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

# Main (Jinja2) template to search DOI.
@app.route("/")
def index():
    code = 200
    doi = None
    err_msg = None
    get_doi = request.args.get("doi")

    # Gather information about submitted DOI ("?doi=" GET parameter).
    if get_doi:
        try:
            doi = DOI(get_doi)
            logger.debug(vars(doi))

        # Handle any errors that may occur.
        except ValueError:
            code = 400
            err_msg = 'Invalid DOI format!'
        except FileNotFoundError:
            code = 404
            err_msg = \
                f'No such DOI (<span class="font-monospace">{get_doi}</span>).'
        except Exception as exc:
            code = 500
            logger.exception(exc)
            err_msg = str(exc)

        # Display any error message that was generated.
        if err_msg:
            flash(err_msg)

    return make_response(render_template("index.html.j2", doi=doi), code)


@app.route('/static/<path:path>')
def statics(path):
    # Static content.
    return send_from_directory("static", path)
