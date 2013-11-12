from bson.objectid import ObjectId

class Mood(object):
    """ Mood CMF type """

    def __init__(self, **kwds):
        self._id = kwds.get('_id', ObjectId())
        self.mood = kwds.get('mood', 'Undefined Mood')


