from tornado.template import Loader
from app.system.handler import BaseHandler
#from app.system.contrib.auth import LoginHandler
import os

data = {}

class IndexHandler(BaseHandler):
    def get(self):
        data['_xsrf']=self.xsrf_token
        self.render("welcome.html", data=data)

class PageHandler(BaseHandler):
    def get(self, slug=None):
        data['_xsrf']=self.xsrf_token
        _page = ".".join((slug, 'html'))
        _abs_page_path = os.path.join(self.get_template_path(), _page)
        if os.path.isfile(_abs_page_path):
            self.render(_page, data=data)
        else:
            self.render("page.html", data=data)

# class AuthHandlerLogin(LoginHandler, BaseHandler):
#     def get(self):
#         if not self.cfg.enable_admin:
#             self.redirect("/")
#         else:
#             self.render("../../static/vendor/inc/login.html", data=data)

# class AuthHandlerLogout(BaseHandler):
#     def get(self):
#         self.clear_all_cookies()
#         self.send_statmsg("Logged out successfully.")
#         self.redirect("/")

