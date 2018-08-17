from .controller import Controller
from service.picture import PictureService


class PictureController(Controller):
    def post(self, request):
        return self.format_response({}), 200
