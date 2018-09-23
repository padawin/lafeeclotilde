from enum import Enum, auto

from model.model import Model, DuplicateFieldError
from model.category import CategoryModel


class CategorySaveResult(Enum):
    OK = auto()
    EMPTY_NAME = auto()
    DUPLICATED_NAME = auto()


class CategoryService:
    def save(self, name, id_category=None):
        name = name.strip()
        if not name:
            return CategorySaveResult.EMPTY_NAME, None
        try:
            if id_category is None:
                CategoryModel.insert({'name': name})
            else:
                CategoryModel.update(
                    {'name': name},
                    ('id_category = %s', [id_category])
                )
        except DuplicateFieldError:
            return CategorySaveResult.DUPLICATED_NAME, None
        Model.commit()
        return CategorySaveResult.OK, None

    def get_all(self):
        categories = CategoryModel.loadAll()
        for category in categories:
            category['date_created'] = (
                category['date_created'].isoformat()
                if category['date_created'] else
                ''
            )
        return categories
