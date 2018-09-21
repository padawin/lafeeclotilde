class CategoryService:
    @staticmethod
    def get_all():
        return {
            'categories': [
                {'id_category': 1, 'name': 'portraits'},
                {'id_category': 2, 'name': 'noir et blanc'},
                {'id_category': 3, 'name': 'paysages'},
            ]
        }
