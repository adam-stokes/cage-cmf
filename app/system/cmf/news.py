from .types import *

class News(object):
    """ News CMF type """
    def __init__(self, **kwds):
        self.title = Blob(kwds['title'])
        self.summary = Blob(kwds['summary'])
        self.body = Blob(kwds['body'])
        self.views = Spinner(kwds['views'])
        self.author = Blob(kwds['author'])
        self.created = DateTime(kwds['created'])
        self.modified = DateTime(kwds['modified'])
        self.expired = DateTime(kwds['expired'])


