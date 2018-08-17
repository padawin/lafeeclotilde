from flask import Blueprint, request

from controller.picture import PictureController


bp = Blueprint('lafeeclotilde', __name__)


@bp.route('/picture', methods=['POST'])
def upload_file():
    controller = PictureController()
    return controller.post(request)
