import unicodedata
import hashlib
import re
import datetime
import calendar
import tornado.web
import markdown2
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from app.system.contrib.util import slugify
from app.models.schema import *

class PageNav(tornado.web.UIModule):
    def render(self):
        return ""

class Slugify(tornado.web.UIModule):
    def render(self, value):
        return slugify(value)

class Syntax(tornado.web.UIModule):
    """ render text through pygments """

    def _unescape_html(self, html):
        html = html.replace('&lt;', '<')
        html = html.replace('&gt;', '>')
        html = html.replace('&amp;', '&')
        html = html.replace('&quot;', '"')
        html = html.replace('&#39;', "'")
        return html

    def css_files(self):
        _css_files = ['/media/vendor/css/highlight.css'] 
        return _css_files
        
    def render(self, html):
        """
        Produces pygmentize syntax highlights
        """
        
        soup = BeautifulSoup(html)
        preblocks = soup.findAll('pre')
        for pre in preblocks:
            if pre.has_key('class'):
                try:
                    code = ''.join([unicode(item) for item in pre.contents])
                    code = _unescape_html(code)
                    lexer = get_lexer_by_name(pre['class'])
                    code_hl = highlight(code, lexer, HtmlFormatter())
                    pre.replaceWith(BeautifulSoup(code_hl))
                except:
                    pass
        return unicode(soup)

class Gravatar(tornado.web.UIModule):
    """ thanks http://www.gregaker.net/2011/feb/16/tornado_gravatar_module/ """
    def render(self, email, size=40, image_type='jpg'):
        email_hash = hashlib.md5(email).hexdigest()
        return "http://gravatar.com/avatar/{0}?s={1}.{2}".format(email_hash, size, image_type)

class MD(tornado.web.UIModule):
    """ renders markdown """
    def render(self, md_str):
        md = markdown2.Markdown(safe_mode='replace')
        return md.convert(md_str)

