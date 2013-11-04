from app.system.cmf.types import *

class User(Entity):
    """ User CMF type """
    def __init__(self, **kwds):
        self.fullname = Blob(kwds['fullname'])
        self.email = Blob(kwds['email'])
        self.apikey = APIKey()
