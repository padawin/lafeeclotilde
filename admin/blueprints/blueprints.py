from flask import Blueprint, render_template, Response, current_app, request

from controller.categories import CategoriesController
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


@bp.route('/categories', methods=['GET'])
def categories():
    controller = CategoriesController(current_app.config)
    res = controller.get()
    return render_template('categories.html', **res)


@bp.route('/photos', methods=['GET'])
def photos():
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
    controller = PicturesController(current_app.config)
    res = controller.get(page)
    return render_template('pictures.html', **res)
