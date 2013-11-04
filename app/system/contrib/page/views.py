from app.system.handler import BaseHandler
from app.system.contrib.util import hash_login, slugify, AttrDict
from app.system.contrib.admin.helpers import AdminHelp
import tornado.web

data={}

# class PageNew(BaseHandler):
#     @tornado.web.authenticated
#     def get(self):
#         self.render("../widgets/page/new.html", data=data)

#     @tornado.web.authenticated
#     def post(self):
#         _c = Page()
#         _c.addon_type = _admin.addons_find(name='page')['_id']
#         _c.name = self.get_argument("pagename")
#         _c.summary = self.get_argument("pagesummary")
#         _c.body = self.get_argument("pagebody")
#         _c.published = True if self.is_argument_present("pagepublished") else False
#         _c.mainnav = True if self.is_argument_present("pagemainnav") else False
#         _c.frontpage = True if self.is_argument_present("frontpage") else False
#         _c.weight = self.get_argument("pageweight") if self.is_argument_present("pageweight") else 0
#         _c.resourceid = slugify(_c.name)
#         _c.c_id = _admin.oid(_admin.client_id)
#         _c_collection = _admin.content_one(resourceid=_c.resourceid)
#         _admin.contents.save(_c.to_python())
#         self.redirect('/admin/page/list')


# class PageEdit(BaseHandler):
#     @tornado.web.authenticated
#     def get(self, page_id):
#         data.content = _admin.content_one(_id=_admin.oid(page_id))
#         self.render("../widgets/page/edit.html", data=data)

#     @tornado.web.authenticated
#     def post(self, page_id):
#         _c = _admin.content_one(_id=_admin.oid(page_id))
#         _c.name = self.get_argument("pagename")
#         _c.summary = self.get_argument("pagesummary")
#         _c.body = self.get_argument("pagebody")
#         _c.published = True if self.is_argument_present("pagepublished") else False
#         _c.mainnav = True if self.is_argument_present("pagemainnav") else False
#         _c.frontpage = True if self.is_argument_present("frontpage") else False
#         _c.weight = self.get_argument("pageweight") if self.is_argument_present("pageweight") else 0
#         _c.resourceid = slugify(_c.name)
#         _c.c_id = _admin.oid(_admin.client_id)
#         _admin.contents.save(_c)
#         self.redirect('/admin/page/edit/%s' % (page_id,))

# class PageList(BaseHandler):
#     @tornado.web.authenticated
#     def get(self):
#         data.content = _admin.content(addon_type=_admin.addons_find(name='page')['_id'])
#         self.render("../widgets/page/list.html", data=data)

hook = dict(
    handlers=list(((r"/admin/page/new/?", 'app.system.contrib.page.views.PageNew'),
                   (r"/admin/page/list/?", 'app.system.contrib.page.views.PageList'),
                   (r"/admin/page/edit/(.*)", 'app.system.contrib.page.views.PageEdit'))))

