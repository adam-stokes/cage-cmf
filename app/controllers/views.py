from tornado.template import Loader
from app.system.handler import BaseHandler
import os

data = {'Index': 'default handler, should be replaced.'}

class IndexHandler(BaseHandler):
    def get(self):
        self.render_json(data)

class EntityHandler(BaseHandler):
    def get(self, cmf_entity_name=None):
        _e = self.load_by_name(cmf_entity_name)
        if not _e:
            return self.render_json({'Error' : 'Unable to find entity %s' % (cmf_entity_name,)})

        self.render_json(list(_e.collection.find(self.query())))

    def post(self, cmf_entity_name=None):
        _e = self.load_by_name(cmf_entity_name)
        if not _e:
            return self.render_json({'Error' : 'Unable to find entity %s' % (cmf_entity_name,)})

        _e.collection.insert(self.query())
        self.render_json({'Success': {'inserted' : self.query()}})

    def put(self, cmf_entity_name=None):
        _e = self.load_by_name(cmf_entity_name)
        if not _e:
            return self.render_json({'Error' : 'Unable to find entity %s' % (cmf_entity_name,)})
        if not self.get_argument('_id'):
            return self.render_json({'Error' : 'No objectid found'})
        _e.collection.save(self.query())
        self.render_json({'Success': {'updated' : self.query()}})
        

