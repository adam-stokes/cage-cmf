import os
import re
import sys
import argparse
import subprocess
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import logging
from app.conf import Config

cfg = Config()

class RunApp(object):
    def __init__(self, commons):
        self.commons = commons
        self.args = self.parse_options(sys.argv)
        self.safe_mode = False
        logging.getLogger().setLevel(logging.DEBUG if self.args.debug else logging.INFO)

    def cmd_project(self, options):
        logging.debug("Setting defaults.")
        if options.rundebugshell or self.safe_mode:
            cmd = [ 'bpython' ]
            logging.info(cmd)
            subprocess.call(cmd, shell=True, executable='/bin/bash')
            return
        if options.runserver:
            _port = options.port if options.port else cfg.port
            logging.debug("Starting local tornado server %s:%s" % (options.server, _port))

            # initialize the application
            http_server = tornado.httpserver.HTTPServer\
                (Application(self.commons['script_location']))
            http_server.listen(_port)
            # enter the Tornado IO loop
            tornado.ioloop.IOLoop.instance().start()

    def parse_options(self, *args, **kwds):
        parser = argparse.ArgumentParser(description='Cage - python powered CMF',
                                         prog='claw')
        parser.add_argument('--debugshell', action='store_true',
                            dest='rundebugshell', default=False,
                            help='Run project shell')
        parser.add_argument('-r', '--runserver', action='store_true',
                            dest='runserver', default=False,
                            help='Run test web server')
        parser.add_argument('-p', '--port', dest='port',
                            help='Port in which server should run on')
        parser.add_argument('--server', dest='server', default="localhost",
                            help='Server hostname of application')
        parser.set_defaults(func=self.cmd_project)

        # Debug commands
        parser.add_argument('-d', '--debug', action='store_true',
                            dest='debug', default=False, help='show debug')
        parser.add_argument('--version', action='version',
                            version=cfg.platform_version,
                            help='Show version')
        return parser.parse_args()

    def run(self):
        # Verify a template is defined and exists.
        if not cfg.template:
            logging.error("No template is defined, probably means no template set in the config.")
            self.safe_mode = True
            logging.info("Attempting to load debugging shell.")
        logging.debug("Template found (%s), parsing arguments." % (cfg.template,))
        self.args.func(self.args)

class Application(tornado.web.Application):
    def __init__(self, cage_path):
        logging.debug("Application path (%s)" % (cage_path,))
        # Set application path in config
        cfg.app_path = cage_path
        # Override template if set in environment
        cfg.template = os.getenv('CAGE_TEMPLATE') if os.getenv('CAGE_TEMPLATE') else cfg.template
        if not os.getenv("CAGE_STATIC_PATH"):
            cfg.static_path = os.path.join(cfg.app_path,
                                           "app",
                                           "static",
                                           cfg.template)
        else:
            cfg.static_path = os.getenv("CAGE_STATIC_PATH")

        if not os.getenv("CAGE_TMPL_PATH"):
            cfg.template_path = os.path.join(cage_path,
                                             "app",
                                             "templates",
                                             cfg.template)
        else:
            cfg.template_path = os.getenv("CAGE_TMPL_PATH")

        urls = [
            (r"/", "app.controllers.views.IndexHandler"),
            (r"/([a-z0-9-]+$)", "app.controllers.views.PageHandler"),
            (r"/media/(.*)", 'tornado.web.StaticFileHandler', {'path' : cfg.static_path}),
            ]

        ui_modules_map = {}
        # some ui_modules have direct relation
        # to enabled addons
        _ui_app = cfg.ui_apps
        for a in _ui_app:
            _ui_modules = __import__("app.ui.%s" % (a,),
                                     globals(),
                                     locals(),
                                     ['ui_modules'],
                                     0)
            try:
                ui_modules = _ui_modules.ui_modules
            except AttributeError:
                # no ui modules exist for application
                continue
            for name in [x for x in dir(ui_modules) if re.findall('[A-Z]\w+', x)]:
                m = getattr(ui_modules, name)
                try:
                    if issubclass(m, tornado.web.UIModule):
                        ui_modules_map[name] = m
                except TypeError:
                    # builtin class
                    pass

        settings = dict(
            template_path=cfg.template_path,
            static_path=cfg.static_path,
            xsrf_cookies=True,
            cookie_secret=cfg.cookie_secret,
            login_url=cfg.login_url,
            debug=cfg.debug,
            ui_modules=ui_modules_map,
            )
        tornado.web.Application.__init__(self, urls, **settings)
        # Database scope
        self.cfg = cfg
