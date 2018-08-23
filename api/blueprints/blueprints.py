from flask import Blueprint, request, current_app

from controller.picture import PictureController
from controller.pictures import PicturesController


bp = Blueprint('lafeeclotilde', __name__)


@bp.route('/picture', methods=['POST'])
def upload_file():
    controller = PictureController(current_app.config)
    return controller.post(request)


@bp.route('/picture', methods=['GET'])
def get_pictures():
    controller = PicturesController(current_app.config)
    return controller.get(request)
