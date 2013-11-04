from tornado.template import Loader
from app.system.handler import BaseHandler
import os

data = {'test_json': 'some test json data'}

class IndexHandler(BaseHandler):
    def get(self):
        self.render_json(data)
