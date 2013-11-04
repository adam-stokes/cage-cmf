class Config(object):
    def __init__(self, **kwds):
        # TODO use kwds to override defaults
        self.login_url = '/auth/login'
        self.ui_apps = ['base']
        self.enable_admin = True
        self.db = { 
            'name' : 'test',
            'conn' : 'mongodb://localhost:27017'
        }
        self.template = 'default'
        self.debug = True
        self.cookie_secret = '45d1d9ed94c34749a95960db2c68c652'
        self.addons = []
        self.platform_version = '1.0.0'
        self.port = 9000
