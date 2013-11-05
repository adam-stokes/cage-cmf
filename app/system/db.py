# DB
from app.conf import Config
from pymongo import MongoClient

class Dbh(object):
    def __init__(self):
        self.db = Config().db
        self.client = MongoClient(self.db['conn'])
        self.environment = "%s-%s" % (self.db['name'],
                                      self.db['env'])
        self.conn = self.client[self.environment]

    def set_collection(self, entity=None):
        return self.conn[entity]
