class ConfigController(object):
    def __init__(self, config):
        self.config = config

    def get(self):
        return {
            'api_host': self.config['API_HOST']
        }
