# CMF types
from datetime import datetime
from bson.json_util import dumps
from app.system.db import Dbh
from app.system.util.loader import load_by_name

class Entity(object):
    """ helper class for converting entities to different formats """
    def __init__(self, cmf_entity_name):
        self.db = Dbh()
        self.entity_name = cmf_entity_name
        self.entity = load_by_name('app.system.cmf.%s' % (self.entity_name,), self.entity_name.capitalize())()

    # private
    def _create_entity(self):
        return load_by_name('app.system.cmf.%s' % (self.entity_name,), self.entity_name.capitalize())()

    def _merge_results(self, results):
        """ multi purpose method to merge mongo results into entity """
        if isinstance(results, list):
            for item in results:
                klass = self._create_entity()
                for k in item.keys():
                    if hasattr(klass, k):
                        setattr(klass, k, item[k])
                return klass
        elif isinstance(results, dict):
            klass = self._create_entity()
            for k in results.keys():
                if hasattr(klass, k):
                    setattr(klass, k, results[k])
            return klass
        else:
            return {'Error' : 'Unable to set attributes'}

    # public
    @property
    def collection(self):
        return self.db.set_collection(self.entity_name)

    @property
    def to_json(self, entity):
        """ converts cmf type to json """
        return dumps(entity, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def find(self, filter_={}):
        return self._merge_results(list(self.collection.find(filter_)))

    def find_one(self, filter_={}):
        return self._merge_results(self.collection.find_one(filter_))

    def save(self, entity):
        return self.collection.save(entity.__dict__)

    def insert(self, entity):
        return self.collection.insert(entity.__dict__)
