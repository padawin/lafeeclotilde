from controller.controller import Controller


class ConfigController(Controller):
    def get(self):
        return {
            'api_host': self.config['API_HOST_FRONTEND']
        }
