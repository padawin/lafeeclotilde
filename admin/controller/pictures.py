from controller.controller import Controller
from service.picture import PictureService


class PicturesController(Controller):
    def get(self):
        service = PictureService(self.config)
        pictures = service.get_all()
        return pictures
