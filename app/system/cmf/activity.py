from app.system.cmf.types import *

class Activity(Entity):
    """ Activity CMF type """
    def __init__(self, **kwds):
        self.status = Blob(kwds.get('status'))
        self.likes = Spinner(kwds.get('likes'))
        self.views = Spinner(kwds.get('views'))

