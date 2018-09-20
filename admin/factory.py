import logging
from flask import Flask, request, url_for
from werkzeug.utils import find_modules, import_string
import http.client as http_client


def create_app(name, settings, **kwargs):
    app = Flask(name, **kwargs)

    app.config.update({})
    app.config.from_envvar(settings, silent=True)

    logger = logging.getLogger("{} logger".format(app.name))
    logger.setLevel(logging.DEBUG)
    logging.info("starting server")

    register_blueprints(app)
    register_logger()
    register_jinja_helpers(app)

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


def register_logger():
    http_client.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def register_jinja_helpers(app):
    def image_url(width, height, crop, path):
        crop = 1 if crop else 0
        return f'/images/{width}x{height}x{crop}/{path}'

    def current_url_paginated(page=None):
        args = request.view_args.copy()
        args['page'] = page
        return url_for(request.endpoint, **args)

    app.jinja_env.globals.update(
        image_url=image_url,
        current_url_paginated=current_url_paginated
    )
