import os
import re
import sys
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.autoreload
from tornado.process import fork_processes, task_id
from tornado.log import app_log
from tornado.options import define, options, parse_command_line
from app.conf import Config

cfg = Config()
define("port", default=9000, help="port", type=int)
define("debug", default=False, help="run in debug mode", type=bool)

class RunApp(object):
    def __init__(self, commons):
        self.commons = commons
        self.commons['safe_mode'] = False
        parse_command_line()

    def run(self):
        if options.debug:
            app_log.setLevel(logging.DEBUG)

        if not options.debug:
            fork_processes(None)
        options.port += task_id() or 0

        app_log.debug("Starting %s on port %s" % (cfg.platform_name, options.port))
        # initialize the application
        tornado.httpserver.HTTPServer(Application(self.commons)).listen(options.port, '0.0.0.0')
        ioloop = tornado.ioloop.IOLoop.instance()
        if options.debug:
            tornado.autoreload.start(ioloop)
        # enter the Tornado IO loop
        ioloop.start()

class Application(tornado.web.Application):
    def __init__(self, commons):
        self.commons = commons
        self.cfg = cfg
        self.cage_path = self.commons['script_location']
        app_log.debug("Application path (%s)" % (self.cage_path,))
        # Set application path in config
        self.cfg.app_path = self.cage_path

        urls = [
            (r"/", "app.controllers.views.IndexHandler"),
            (r"/entity/([A-Za-z0-9-]+$)", "app.controllers.views.EntityHandler"),
            ]

        ui_modules_map = {}
        settings = dict(
            template_path=None,
            static_path=None,
            xsrf_cookies=True,
            cookie_secret=self.cfg.cookie_secret,
            debug=options.debug,
            ui_modules=ui_modules_map,
            )
        tornado.web.Application.__init__(self, urls, **settings)
