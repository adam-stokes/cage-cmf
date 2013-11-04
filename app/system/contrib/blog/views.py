from app.system.handler import BaseHandler
from app.system.contrib.util import hash_login, slugify, AttrDict
from app.system.contrib.admin.helpers import AdminHelp
from app.system.contrib.storage import S3
from app.models.schema import *
import tornado.web

data=AttrDict()
_admin=AdminHelp()

class BlogNew(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("../widgets/blog/new.html", data=data)

    @tornado.web.authenticated
    def post(self):
        _c = Blog()
        _c.addon_type = _admin.addons_find(name='blog')['_id']
        _c.name = self.get_argument("name")
        _c.body = self.get_argument("body")
        _c.published = True if self.is_argument_present("published") else False
        _c.resourceid = slugify(_c.name)
        _c.c_id = _admin.oid(_admin.client_id)
        _c_collection = _admin.content_one(resourceid=_c.resourceid)
        _admin.contents.save(_c.to_python())
        self.redirect('/admin/blog/list')


class BlogEdit(BaseHandler):
    @tornado.web.authenticated
    def get(self, blog_id):
        data.content = _admin.content_one(_id=_admin.oid(blog_id))
        self.render("../widgets/blog/edit.html", data=data)

    @tornado.web.authenticated
    def post(self, blog_id):
        _c = _admin.content_one(_id=_admin.oid(blog_id))
        _c.name = self.get_argument("name")
        _c.body = self.get_argument("body")
        _c.published = True if self.is_argument_present("published") else False
        _c.resourceid = slugify(_c.name)
        _c.c_id = _admin.oid(_admin.client_id)
        _admin.contents.save(_c)
        self.redirect('/admin/blog/edit/%s' % (blog_id,))

class BlogList(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        data.content = _admin.content(addon_type=_admin.addons_find(name='blog')['_id'])
        self.render("../widgets/blog/list.html", data=data)

hook = dict(
    handlers=list(((r"/admin/blog/new/?", 'app.system.contrib.blog.views.BlogNew'),
                   (r"/admin/blog/list/?", 'app.system.contrib.blog.views.BlogList'),
                   (r"/admin/blog/edit/(.*)", 'app.system.contrib.blog.views.BlogEdit'))))

