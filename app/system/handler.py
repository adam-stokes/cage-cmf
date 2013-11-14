import tornado.web
import logging
import os
from bson.json_util import dumps, loads
from tornado.escape import to_unicode
from tornado.template import Loader
from tornado.log import app_log
from app.system.util.loader import load_by_name

class BaseHandler(tornado.web.RequestHandler):
    @property
    def cfg(self):
        return self.application.cfg

    def head(self, *args, **kwargs):
        self.get(*args, **kwargs)
        self.request.body = ''

    def is_argument_present(self, name):
        return not (self.request.arguments.get(name, None) == None)

    def query(self):
        _filtered = {}
        for k in self.request.arguments.keys():
            _filtered[k] = self.get_argument(k)
        return _filtered

    def load_by_name(self, name):
        try:
            return load_by_name('app.system.cmf.%s' % (name.lower(),),
                                name.capitalize())()
        except ImportError as e:
            app_log.debug(e)
            return False

    # Page render
    def render(self, template_name, **kwargs):
        tornado.web.RequestHandler.render(self,
                                          template_name,
                                          **kwargs)

    # API render
    def render_json(self, content):
        content_json = dumps(content)
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(content_json)
        self.finish()

