from controller.controller import Controller
from service.picture import PictureService


class PicturesController(Controller):
    def get(self, page):
        if page is None:
            page = 1

        nb_pictures = self.config['PICTURES_PER_PAGE']
        first_picture = (page - 1) * nb_pictures
        service = PictureService(self.config)
        pictures = service.get_all(first_picture, nb_pictures)
        return pictures
