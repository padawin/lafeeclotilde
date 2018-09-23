from enum import Enum, auto

from model.model import Model, DuplicateFieldError
from model.category import CategoryModel


class CategorySaveResult(Enum):
    OK = auto()
    EMPTY_NAME = auto()
    DUPLICATED_NAME = auto()


class CategoryService:
    def save(self, name):
        name = name.strip()
        if not name:
            return CategorySaveResult.EMPTY_NAME, None
        try:
            CategoryModel.insert({'name': name})
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
