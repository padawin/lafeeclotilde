import json
import requests


class CategoryService:
    def __init__(self, config):
        self.config = config

    def get_all(self):
        url = "{host}{endpoint}".format(
            host=self.config['API_HOST_BACKEND'], endpoint='/categories'
        )
        response = requests.request('GET', url)
        return json.loads(response.content)
