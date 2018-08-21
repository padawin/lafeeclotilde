import logging
from flask import Flask, current_app, abort
from flask_cors import CORS
from werkzeug.utils import find_modules, import_string
import http.client as http_client

from model import model


def create_app(name, settings, **kwargs):
    app = Flask(name, **kwargs)

    app.config.update({})
    app.config.from_envvar(settings, silent=True)

    logger = logging.getLogger("{} logger".format(app.name))
    logger.setLevel(logging.DEBUG)
    logging.info("starting server")

    register_setup(app)
    register_blueprints(app)
    register_logger()
    register_cors(app)

    return app


def register_blueprints(app):
    """Register all blueprint modules

    Reference: Armin Ronacher, "Flask for Fun and for Profit" PyBay 2016.
    """
    for name in find_modules('blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None


def register_cors(app):
    CORS(app, origins=app.config['CORS_ORIGINS'])


def register_logger():
    http_client.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def register_setup(app):
    @app.before_request
    def get_db():
        logging.info("Creating DB connection")
        try:
            model.Model.connect("dbname={} user={} host={} password={}".format(
                current_app.config['DATABASE_NAME'],
                current_app.config['DATABASE_USER'],
                current_app.config['DATABASE_HOST'],
                current_app.config['DATABASE_PASSWORD']
            ))
        except model.ConnectionError as e:
            logging.error(
                "Failed connecting to database {} at {} with: {}".format(
                    current_app.config['DATABASE_NAME'],
                    current_app.config['DATABASE_HOST'],
                    str(e)
                )
            )
            abort(500)


def register_teardowns(app):
    @app.teardown_appcontext
    def close_db(error):
        logging.info("Disconnecting DB connection")
        model.Model.disconnect()
