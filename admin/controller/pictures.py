import math

from controller.controller import Controller
from service.picture import PictureService
from tools.pagination import Pagination


class PicturesController(Controller):
    def get(self, page):
        if page is None:
            page = 1

        nb_pictures = self.config['PICTURES_PER_PAGE']
        first_picture = (page - 1) * nb_pictures
        service = PictureService(self.config)
        pictures = service.get_all(first_picture, nb_pictures)
        for picture in pictures['pictures']:
            directory, file_name, _ = service.get_storage_path(picture)
            picture['url'] = f'{directory}/{file_name}'

        pagination = Pagination(
            page, math.ceil(pictures['total_count'] / nb_pictures)
        )
        return {'pictures': pictures['pictures'], 'pagination': pagination}
