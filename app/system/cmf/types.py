# CMF types
from app.system.db import Dbh

class Entity(object):
    """ helper class for converting entities to different formats """

    # public
    @property
    def db(self):
        return Dbh()

    @classmethod
    def name(class_):
        try:
            return class_.cmf_name.lower()
        except AttributeError:
            return class_.__name__.lower()

    @property
    def collection(self):
        """ our collection manager """
        return self.db.set_collection(self.name())
