from bson.objectid import ObjectId
from datetime import datetime

class Media(object):
    """ Media CMF type """

    def __init__(self, **kwds):
        self._id = kwds.get('_id', ObjectId())
        self.title = kwds.get('title', 'Media title')
        self.path = kwds.get('path', 'Media Path')
        self.size = kwds.get('size', 'Media Size')
        self.thumbnail = kwds.get('thumbnail', 'Thumbnail Size')
        self.created = kwds.get('created', datetime.now())
