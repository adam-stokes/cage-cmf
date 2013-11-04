import tornado.web
import logging
import os
import json
from tornado.escape import to_unicode
from tornado.template import Loader

class BaseHandler(tornado.web.RequestHandler):
    @property
    def cfg(self):
        return self.application.cfg

    def head(self, *args, **kwargs):
        self.get(*args, **kwargs)
        self.request.body = ''

    def is_argument_present(self, name):
        return not (self.request.arguments.get(name, None) == None)
        
    # Page render
    def render(self, template_name, **kwargs):
        tornado.web.RequestHandler.render(self,
                                          template_name,
                                          **kwargs)

    # API render
    def render_json(self, content):
        content_json = json.dumps(content)
        self.set_header("Content-Type", "application/json")
        if self.is_argument_present("callback"):
            self.write('%s(%s)' % (self.get_argument('callback'), content))
        else:
            self.write(content)


