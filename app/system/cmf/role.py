""" The role type is intended to be used for user level/subscription sites.

For example,

user1 has a role of staff - for staff related tasks like adding pages/news
user1 has a role of member1 - for member1 or lower restricted data
"""
from bson.objectid import ObjectId
from datetime import datetime

class Role(object):
    """ Role CMF type """
    def __init__(self, **kwds):
        self._id = kwds.get('_id', ObjectId())
        self.created = kwds.get('created', datetime.now())
        self.modified = kwds.get('modified', datetime.now())
        self.name = kwds.get('name', 'No role set')
