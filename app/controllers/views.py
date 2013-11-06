from tornado.template import Loader
from app.system.handler import BaseHandler
from app.system.cmf.types import Entity
import os

data = {'Index': 'default handler, should be replaced.'}

class IndexHandler(BaseHandler):
    def get(self):
        self.render_json(data)

class EntityHandler(BaseHandler):
    def get(self, cmf_entity_name=None):
        if not cmf_entity_name:
            self.render_json({'Error' : 'No entity was defined'})
        self.render_json(entity.find()[s])
