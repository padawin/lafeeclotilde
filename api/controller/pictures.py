from .controller import Controller
from service.picture import PictureService


class PicturesController(Controller):
    def get(self, request):
        service = PictureService(self.config)
        pictures, total_count = service.get_all(
            request.args.get('offset', 0),
            request.args.get('limit', 10)
        )
        return self.format_response(
            {
                'pictures': pictures,
                'total_count': total_count
            }
        ), 200
