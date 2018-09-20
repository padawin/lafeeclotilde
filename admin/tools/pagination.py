# http://flask.pocoo.org/snippets/44/


class Pagination:
    def __init__(self, current_page, count_pages):
        self.page = current_page
        self.count_pages = count_pages

    def has_prev(self):
        return self.page > 1

    def has_next(self):
        return self.page < self.count_pages

    def iter_pages(self):
        for page in range(1, self.count_pages + 1):
            yield page
