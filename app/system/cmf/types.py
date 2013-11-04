# CMF types
from datetime import datetime

class Blob(object):
    def __init__(self, data):
        self.data = data
        self.cols = 40
        self.rows = 5

class DateTime(object):
    def __init__(self, data):
        self.data = data

class Password(object):
    def __init__(self, data):
        self.data = data

class Spinner(object):
    def __init__(self, count):
        self.count = count
