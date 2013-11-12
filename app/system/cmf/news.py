from bson.objectid import ObjectId
from datetime import datetime

class News(object):
    """ News CMF type """
    def __init__(self, **kwds):
        self._id = kwds.get('_id', ObjectId())
        self.title = kwds.get('title', 'Undefined title')
        self.summary = kwds.get('summary', 'Undefined summary')
        self.content = kwds.get('content', 'Undefined content')
        self.author = kwds.get('author', 'Undefined author')
        self.published = kwds.get('published', datetime.now())
        self.created = kwds.get('created', datetime.now())
        self.modified = kwds.get('modified', datetime.now())
        self.comments = []
