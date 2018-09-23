from flask import Blueprint, request, current_app

from controller.picture import PictureController
from controller.pictures import PicturesController
from controller.category import CategoryController
from controller.categories import CategoriesController


bp = Blueprint('lafeeclotilde', __name__)


@bp.route('/picture', methods=['POST'])
def upload_file():
    controller = PictureController(current_app.config)
    return controller.post(request)


@bp.route('/pictures', methods=['GET'])
def get_pictures():
    controller = PicturesController(current_app.config)
    return controller.get(request)


@bp.route('/category', methods=['POST'])
def create_category():
    controller = CategoryController(current_app.config)
    return controller.post(request)


@bp.route('/category/<int:id_category>', methods=['PUT'])
def update_category(id_category):
    controller = CategoryController(current_app.config)
    return controller.put(request, id_category)


@bp.route('/categories', methods=['GET'])
def get_categories():
    controller = CategoriesController(current_app.config)
    return controller.get(request)
