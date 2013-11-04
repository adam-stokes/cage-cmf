from tornado.template import Loader
from app.system.handler import BaseHandler
import os

data = {'info': 'default handler, should be replaced.'}

class IndexHandler(BaseHandler):
    def get(self):
        self.render_json(data)
