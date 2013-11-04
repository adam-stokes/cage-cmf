import tornado.web
import logging
import os
from tornado.escape import to_unicode
from tornado.template import Loader

class BaseHandler(tornado.web.RequestHandler):
    @property
    def session(self):
        return self.application

    @property
    def cfg(self):
        return self.application.cfg

    # def get_node_by_slug(self, slug):
    #     try:
    #         _node = self.session\
    #             .query(Node)\
    #             .filter_by(resourceid=slug,
    #                        client_id=self.client.id).one()
    #         logging.debug("node: %d, %s" % (_node.id, _node.name))
    #     except NoResultFound:
    #         _node = None
    #     return _node

    # def get_content_from_node(self, node):
    #     try:
    #         _content = self.session\
    #             .query(Content)\
    #             .filter(Content.node==node).one()
    #         logging.debug("content: %d, nodeid(%d)" % (_content.id, _content.node_id))
    #     except NoResultFound:
    #         _content = None
    #     return _content

    def get_current_user(self):
        return to_unicode(self.get_secure_cookie('userid'))

    # @property
    # def get_current_username(self):
    #     return to_unicode(self.client.username)

    # @property
    # def is_staff(self):
    #     return self.client.is_staff
        
    # def validate_passwords(self):
    #     if not (self.is_argument_present("password") and self.is_argument_present("confirm_password")):
    #         return False
    #     if not (self.get_argument("password") == self.get_argument("confirm_password")):
    #         return False
    #     return True
        
    def head(self, *args, **kwargs):
        self.get(*args, **kwargs)
        self.request.body = ''

    def get_secure_cookie(self, name, if_none=""):
        cook = tornado.web.RequestHandler.get_secure_cookie(self, name)
        if cook == None:
            return if_none
        return cook

    def is_argument_present(self, name):
        return not (self.request.arguments.get(name, None) == None)
        
    def send_errmsg(self, errmsg):
        self.set_secure_cookie("errmsg", errmsg)
        
    def send_statmsg(self, statmsg):
        self.set_secure_cookie("statmsg", statmsg)

    def render(self, template_name, **kwargs):
        error = self.get_secure_cookie("errmsg")
        status = self.get_secure_cookie("statmsg")
        self.clear_cookie("errmsg")
        self.clear_cookie("statmsg")
        tornado.web.RequestHandler.render(self,
                                          template_name,
                                          errmsg=error,
                                          statmsg=status,
                                          **kwargs)



