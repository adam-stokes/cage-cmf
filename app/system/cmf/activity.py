from bson.objectid import ObjectId
class Activity(object):
    """ Activity CMF type """

    def __init__(self, **kwds):
        self._id = kwds.get('_id', ObjectId())
        self.status = kwds.get('status', 'Undefined Status')
        self.likes = kwds.get('likes', 0)

