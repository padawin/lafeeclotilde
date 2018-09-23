from controller.controller import Controller
from service.category import CategoryService


class CategoriesController(Controller):
    def get(self):
        service = CategoryService(self.config)
        categories = service.get_all()
        return categories
