from service.category import CategoryService


class CategoriesController:
    def get(self):
        service = CategoryService()
        categories = service.get_all()
        return categories
