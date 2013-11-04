from app.system.cmf.types import *

class News(Entity):
    """ News CMF type """
    def __init__(self, **kwds):
        self.title = Blob(kwds.get('title'))
        self.summary = Blob(kwds.get('summary'))
        self.body = Blob(kwds.get('body'))
        self.views = Spinner(kwds.get('views'))
        self.author = Blob(kwds.get('author'))
        self.created = DateTime(kwds.get('created'))
        self.modified = DateTime(kwds.get('modified'))
        self.expired = DateTime(kwds.get('expired'))
        self.tags = List(kwds.get('tags', ['Undefined']))


