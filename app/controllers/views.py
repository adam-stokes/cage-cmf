from tornado.log import app_log
from app.system.handler import BaseHandler
import os

data = {'Index': 'default handler, should be replaced.'}

class IndexHandler(BaseHandler):
    def get(self):
        self.render_json(data)

class EntityHandler(BaseHandler):
    """ route handler for non filtered listing of entity """
    def get(self, cmf_entity_name=None):
        _e = self.load_by_name(cmf_entity_name)
        if not _e:
            return self.render_json({'Error' : \
                                     'Unable to find entity %s' % (cmf_entity_name,)})

        self.render_json(list(_e.collection.find())[:100])

class EntityNewHandler(BaseHandler):
    def post(self, cmf_entity_name=None):
        app_log.debug("POST found for new handler")
        _e = self.load_by_name(cmf_entity_name)
        if not _e:
            return self.render_json({'Error' : \
                                     'Unable to find entity %s' % (cmf_entity_name,)})

        _e.collection.insert(self.query())
        self.render_json({'Success': {'inserted' : self.query()}})

class EntitySearchHandler(BaseHandler):
    def get(self, cmf_entity_name=None):
        _e = self.load_by_name(cmf_entity_name)
        if not _e:
            return self.render_json({'Error' : \
                                     'Unable to find entity %s' % (cmf_entity_name,)})
        if self.is_argument_present('oid'):
            return self.render_json(_e.collection.find({'_id' : \
                                                        _e.to_oid(self.get_argument('oid'))}))
        self.render_json(_e.collection.find(self.query()))

class EntityModifyHandler(BaseHandler):
    def put(self, cmf_entity_name=None, oid=None):
        _e = self.load_by_name(cmf_entity_name)
        if not _e:
            return self.render_json({'Error' : \
                                     'Unable to find entity %s' % (cmf_entity_name,)})
        _e.collection.update({'_id' : _e.to_oid(oid)}, {"$set" :self.query()})
        self.render_json({'Success': {'updated' : self.query()}})
        
    def delete(self, cmf_entity_name=None, oid=None):
        _e = self.load_by_name(cmf_entity_name)
        if not _e:
            return self.render_json({'Error' : \
                                     'Unable to find entity %s' % (cmf_entity_name,)})
        _e.collection.remove({'_id' : _e.to_oid(oid)})
        self.render_json({'Success': {'removed' : oid}})
