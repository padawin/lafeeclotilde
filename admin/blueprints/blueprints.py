from flask import Blueprint, render_template, Response, current_app

from controller.config import ConfigController


bp = Blueprint('lafeeclotilde', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/config.js')
def config():
    controller = ConfigController(current_app.config)
    return Response(
        render_template('config.js', data=controller.get()),
        mimetype='application/javascript'
    )
