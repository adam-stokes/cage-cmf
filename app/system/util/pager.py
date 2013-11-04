class Pagination(object):
    def __init__(self, page, row_limit, skip_limit, posts=None):
        self.page = int(page)
        self.row_limit = int(row_limit)
        self.skip_limit = (int(self.page) - 1) * skip_limit 
        self.posts = posts
        try:
            self.count = self.posts.count()
        except AttributeError:
            self.count = 0

    @property
    def pages(self):
        return self.count / self.page
        
    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages
