# CMF types
from datetime import datetime
import json
from app.system.encryption import decrypt, encrypt

class Entity(object):
    def to_json(self):
        """ converts cmf type to json """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def to_yaml(self):
        """ converts cmf type to yaml """
        pass

class Blob(object):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "%s" % (self.data,)

    def __repr__(self):
        return self.__str__()

class DateTime(object):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "%s" % (self.data,)

    def __repr__(self):
        return self.__str__()

class APIKey(object):
    """ api key type """
    def __str__(self):
        return "not implemented"
        
    def __call__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

class Spinner(object):
    def __init__(self, count):
        self.count = count

    def __str__(self):
        return "%s" % (str(self.count),)
    
    def __repr__(self):
        return self.__str__()

class List(list):
    def __init__(self, data):
        self.data = data
