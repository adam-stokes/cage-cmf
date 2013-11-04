from app.system.cmf.types import *

class Page(Entity):
    """ Page CMF type """
    def __init__(self, **kwds):
        self.title = Blob(kwds['title'])
        self.summary = Blob(kwds['summary'])
        self.body = Blob(kwds['body'])
        self.author = Blob(kwds['author'])
        self.created = DateTime(kwds['created'])
        self.modified = DateTime(kwds['modified'])
        self.views = Spinner(kwds['views'])
