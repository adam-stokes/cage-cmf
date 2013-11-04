from .types import *

class Activity(object):
    """ Activity CMF type """
    def __init__(self, **kwds):
        self.status = Blob(kwds['status'])
        self.likes = Spinner(kwds['likes'])
        self.views = Spinner(kwds['views'])

