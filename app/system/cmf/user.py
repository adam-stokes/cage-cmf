from bson.objectid import ObjectId
from datetime import datetime

class User(object):
    """ User CMF type """
    def __init__(self, **kwds):
        self._id = kwds.get('_id', ObjectId())
        self.created = kwds.get('created', datetime.now())
        self.modified = kwds.get('modified', datetime.now())
        self.name = kwds.get('name', 'Who dat?')
        self.email = kwds.get('email')


