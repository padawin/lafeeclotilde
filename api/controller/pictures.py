from .controller import Controller
from service.picture import PictureService


class PicturesController(Controller):
    def get(self, request):
        service = PictureService(self.config)
        res = service.get_all(
            request.args.get('offset', 0),
            request.args.get('limit', 10)
        )
        return self.format_response(res), 200
