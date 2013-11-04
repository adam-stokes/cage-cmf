# Deprecated, everyone should be using built in web server behind
# a proxy like nginx.
import warnings
warnings.warn("deprecated", DeprecationWarning)

import os
import sys
import uuid
sys.path.insert(0,os.path.abspath("%s/.." % os.path.abspath(os.path.dirname(__file__))))

import site
site.addsitedir("%s/../env/lib/python2.7/site-packages" % os.path.abspath(os.path.dirname(__file__)))

import wsgiref.handlers
import tornado.wsgi

# preload views
from app.controllers import urls as controller_urls 
from app.api import urls as api_urls
from app.conf import TEMPLATE_THEME

urls = controller_urls.patterns + api_urls.patterns

settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'templates', TEMPLATE_THEME),
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
    'cookie_secret': '45d1d9ed94c34749a95960db2c68c652',
    'xsrf_cookies': True,
    'login_url' : '/user/login',
}

application = tornado.wsgi.WSGIApplication(urls, **settings)

wsgiref.handlers.CGIHandler().run(application)
