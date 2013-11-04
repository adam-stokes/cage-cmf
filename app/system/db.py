# DB
from app.conf import Config
from pymongo import MongoClient

class Dbh(object):
    def __init__(self, commons):
        self.commons = commons
        self.db = Config().db
        self.client = MongoClient(self.db['conn'])

    def testdb(self):
        self.client[self.db['name']+'-test']

    def stagedb(self):
        self.client[self.db['name']+'-stage']

    def proddb(self):
        self.client[self.db['name']]
        
