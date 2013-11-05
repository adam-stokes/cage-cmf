from tornado.template import Loader
from app.system.handler import BaseHandler
import os

data = {'Index': 'default handler, should be replaced.'}

class IndexHandler(BaseHandler):
    def get(self):
        self.render_json(data)

class EntityHandler(BaseHandler):
    def get(self, cmf_entity=None):
        self.render_json(data)
