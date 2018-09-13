import json
import requests


class PictureService:
    def __init__(self, config):
        self.config = config

    def get_all(self, first_picture, nb_pictures):
        url = "{host}{endpoint}".format(
            host=self.config['API_HOST'], endpoint='/pictures'
        )
        response = requests.request(
            'GET', url, params={'offset': first_picture, 'limit': nb_pictures}
        )
        return json.loads(response.content)
