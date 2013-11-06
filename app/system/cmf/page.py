from bson.objectid import ObjectId
from datetime import datetime

class Page(object):
    """ SinglePage CMF type """

    def __init__(self, **kwds):
        self._id = kwds.get('_id', ObjectId())
        self.title = kwds.get('title', 'SinglePage Document')
        self.user = kwds.get('author', 'undef user')
        self.content = kwds.get('content', 'Undefined content')
        self.published = kwds.get('published', datetime.now())
        self.created = kwds.get('created', datetime.now())
        self.modified = kwds.get('modified', datetime.now())
        self.seo_description = kwds.get('seo_description', 'SEO Description')
        self.seo_keywords = kwds.get('seo_keywords', 'SEO Keywords')
