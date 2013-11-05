""" Pages Type for defining structured single or multi page documents """

class Page(object):
    """ SinglePage CMF type """

    type_name = 'Page'

    def __init__(self, **kwds):
        self.title = kwds.get('title', 'SinglePage Document')
        self.author = kwds.get('author', 'Undefined author')
        self.content = kwds.get('content', 'Undefined content')
