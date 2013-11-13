""" The role type is intended to be used for user level/subscription sites.

For example,

user1 has a role of staff - for staff related tasks like adding pages/news
user1 has a role of member1 - for member1 or lower restricted data
"""
from app.system.cmf.types import Entity

class Role(Entity):
    """ Role CMF type """
    pass
