# CMF types
from datetime import datetime
from app.system.db import Dbh
from app.system.util.loader import load_by_name

class Entity(object):
    """ helper class for converting entities to different formats """
    def __init__(self, cmf_entity):
        self.db = Dbh()
        self.entity_name = self._to_name(cmf_entity)
        self.entity = load_by_name('app.system.cmf.%s' % (self.entity_name,), self.entity_name.capitalize())

    def _to_name(self, entity_name):
        try:
            return entity_name.__name__.lower()
        except AttributeError:
            return entity_name

    def _merge_results(self, results):
        """ multi purpose method to merge mongo results into entity """
        if isinstance(results, list):
            res_list = []
            for item in results:
                klass = self.entity()
                for k in item.keys():
                    if hasattr(klass, k):
                        setattr(klass, k, item[k])
                res_list.append(klass)
            return res_list
        elif isinstance(results, dict):
            klass = self.entity()
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

    def find(self, filter_={}):
        """ Returns list of entities """
        return self._merge_results(list(self.collection.find(filter_)))

    def find_one(self, filter_={}):
        """ Returns 1 entity result """
        return self._merge_results(self.collection.find_one(filter_))

    def save(self, entity):
        """ Saves single entity """
        return self.collection.save(entity.__dict__)

    def save_batch(self, entities):
        """ Saves list of entities """
        if not isinstance(entities, list):
            return {'Error' : 'Cannot batch save as not list was found.'}
        else:
            results = []
            for item in entities:
                oid = self.collection.save(item.__dict__)
                results.append({'Saved' : str(oid)})
            return results
