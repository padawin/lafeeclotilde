import json

from .controller import Controller
from service.category import CategoryService, CategorySaveResult


class CategoryController(Controller):
    def post(self, request):
        return self._save(request)

    def put(self, request, id_category):
        return self._save(request, id_category)

    def delete(self, request, id_category):
        service = CategoryService()
        service.delete(id_category)
        return self.format_response(dict()), 200

    def _save(self, request, id_category=None):
        service = CategoryService()
        try:
            data = json.loads(request.data)
        except json.decoder.JSONDecodeError as e:
            return json.dumps({'error': str(e)}), 400
        try:
            name = data['name']
        except KeyError:
            return json.dumps({'error': 'Missing Category name'}), 400

        res = service.save(name, id_category)
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
