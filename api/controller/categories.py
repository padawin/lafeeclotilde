from .controller import Controller
from service.category import CategoryService


class CategoriesController(Controller):
    def get(self, request):
        service = CategoryService()
        categories = service.get_all()
        return self.format_response({'categories': categories}), 200
