from tornado.template import Loader
from app.system.handler import BaseHandler
import os

data = {'info': 'default handler, should be replaced.'}

class IndexHandler(BaseHandler):
    def get(self):
        self.render_json(data)

class TypeHandler(BaseHandler):
    def get(self, type_name=None):
        self.render_json({'type handler' : 'not implemented.'})

class EntityHandler(BaseHandler):
    def get(self, cmf_entity=None):
        self.render_json({'entity handler' : 'not implemented.'})
