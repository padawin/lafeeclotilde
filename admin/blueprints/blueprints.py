from flask import Blueprint, render_template, Response, current_app

from controller.config import ConfigController
from controller.pictures import PicturesController


bp = Blueprint('lafeeclotilde', __name__)


@bp.route('/')
def index(methods=['GET']):
    return render_template('index.html')


@bp.route('/config.js', methods=['GET'])
def config():
    controller = ConfigController(current_app.config)
    return Response(
        render_template('config.js', data=controller.get()),
        mimetype='application/javascript'
    )


@bp.route('/photos', methods=['GET'])
def photos():
    controller = PicturesController(current_app.config)
    return render_template('pictures.html', pictures=controller.get())
