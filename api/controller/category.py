import json

from .controller import Controller
from service.category import CategoryService, CategorySaveResult


class CategoryController(Controller):
    def post(self, request):
        service = CategoryService()
        try:
            data = json.loads(request.data)
        except json.decoder.JSONDecodeError as e:
            return json.dumps({'error': str(e)}), 400
        try:
            name = data['name']
        except KeyError:
            return json.dumps({'error': 'Missing Category name'}), 400

        res = service.save(name)
        body, status = self.create_response(res, {
            CategorySaveResult.OK: {},
            CategorySaveResult.EMPTY_NAME: (
                "Le nom de la categorie ne peut pas etre vide", 400
            ),
            CategorySaveResult.DUPLICATED_NAME: (
                "Une categorie existe deja avec nom", 400
            )
        })
        return self.format_response(body), status
