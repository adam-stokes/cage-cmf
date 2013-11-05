import os
import re
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.log import app_log
from tornado.options import define, options, parse_command_line
from app.conf import Config

cfg = Config()
define("port", default=9000, help="port", type=int)

class RunApp(object):
    def __init__(self, commons):
        self.commons = commons
        self.commons['args'] = parse_command_line()
        self.commons['safe_mode'] = False

    def run(self):
        # Verify a template is defined and exists.
        if not cfg.template:
            app_log.error("No template is defined, probably means no template set in the config.")
            self.commons['safe_mode'] = True
            app_log.info("Attempting to load debugging shell.")
        app_log.debug("Template found (%s), parsing arguments." % (cfg.template,))
        _port = options.port if options.port else cfg.port
        app_log.debug("Starting local tornado server on port %s" % (_port,))

        # initialize the application
        http_server = tornado.httpserver.HTTPServer\
                      (Application(self.commons))
        http_server.listen(_port)
        # enter the Tornado IO loop
        tornado.ioloop.IOLoop.instance().start()

class Application(tornado.web.Application):
    def __init__(self, commons):
        self.commons = commons
        self.cfg = cfg
        self.cage_path = self.commons['script_location']
        app_log.debug("Application path (%s)" % (self.cage_path,))
        # Set application path in config
        self.cfg.app_path = self.cage_path
        # Override template if set in environment
        self.cfg.template = os.getenv('CAGE_TEMPLATE') if os.getenv('CAGE_TEMPLATE') else cfg.template
        if not os.getenv("CAGE_STATIC_PATH"):
            self.cfg.static_path = os.path.join(self.cfg.app_path,
                                           "app",
                                           "static",
                                           self.cfg.template)
        else:
            self.cfg.static_path = os.getenv("CAGE_STATIC_PATH")

        if not os.getenv("CAGE_TMPL_PATH"):
            self.cfg.template_path = os.path.join(self.cage_path,
                                             "app",
                                             "templates",
                                             self.cfg.template)
        else:
            self.cfg.template_path = os.getenv("CAGE_TMPL_PATH")

        urls = [
            (r"/", "app.controllers.views.IndexHandler"),
            (r"/entity/([A-Za-z0-9-]+$)", "app.controllers.views.EntityHandler"),
            (r"/media/(.*)", 'tornado.web.StaticFileHandler', {'path' : self.cfg.static_path}),
            ]

        ui_modules_map = {}
        settings = dict(
            template_path=self.cfg.template_path,
            static_path=self.cfg.static_path,
            xsrf_cookies=True,
            cookie_secret=self.cfg.cookie_secret,
            debug=self.cfg.debug,
            ui_modules=ui_modules_map,
            )
        tornado.web.Application.__init__(self, urls, **settings)
