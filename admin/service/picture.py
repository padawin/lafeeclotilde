import json
import requests


class PictureService:
    def __init__(self, config):
        self.config = config

    def get_all(self):
        url = "{host}{endpoint}".format(
            host=self.config['API_HOST'], endpoint='/picture'
        )
        response = requests.request('GET', url)
        return json.loads(response.content)
