from app.system.handler import BaseHandler
from app.system.contrib.auth import LoginHandler
from app.system.log import logger as watchdog
from app.system.contrib.util import hash_login, slugify, AttrDict
import tornado.web
from datetime import datetime
import os
import urllib
import logging
import json

data = {}

# Global Deletion for any specified content
class AdminContentDelete(BaseHandler):
    @tornado.web.authenticated
    def get(self, page_id):
        try:
            _del_page = self.session.query(Node).filter_by(id=page_id).one()
            self.session.delete(_del_page)
            self.session.commit()
        except NoResultFound:
            self.send_errmsg("No content found by this id.")
        self.redirect(self.request.headers['Referer'])

# REST response for editable
class AdminContentEdit(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        self.write(self.get_argument('value'))

class AdminContentUpdate(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        """
        handles entering content plus some attributes
        to database
        """
        name = self.get_argument('pagetitle')
        body = self.get_argument('body')
        node_id = self.get_argument('_id') if self.is_argument_present('_id') else None
        resourceid = slugify(name)
        logging.debug("DB: attempting to find: %s" % (resourceid,))
        if node_id:
            _node = self.session.query(Node).filter_by(id=node_id).one()
        else:
            logging.debug('No node found.')
            _node = Node(resourceid)

        try:
            _content = self.session\
                .query(Content)\
                .filter(Content.node==_node)\
                .one()
        except:
            _content = Content()
            _content.node = _node

        _content.node.name = name
        _content.node.resourceid = resourceid
        _content.node.published = True if self.is_argument_present('published') else False
        _content.node.mainnav = True if self.is_argument_present('mainnav') else False
        _content.node.splash_page = True if self.is_argument_present('splash_page') else False
        _content.node.client = self.client
        _content.body = body
        self.session.add(_content)
        self.session.commit()
        self.redirect("/%s" % (resourceid,))
