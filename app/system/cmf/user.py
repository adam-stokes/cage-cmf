from .types import *

class User(object):
    """ User CMF type """
    def __init__(self, **kwds):
        self.fullname = Blob(kwds['fullname'])
        self.email = Blob(kwds['email'])
        self.password = Password(kwds['password'])
