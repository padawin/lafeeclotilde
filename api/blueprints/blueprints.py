from flask import Blueprint, request, current_app

from controller.picture import PictureController


bp = Blueprint('lafeeclotilde', __name__)


@bp.route('/picture', methods=['POST'])
def upload_file():
    controller = PictureController(current_app.config)
    return controller.post(request)
