class Config(object):
    def __init__(self, **kwds):
        # TODO use kwds to override defaults
        self.ui_apps = ['base']
        self.enable_admin = True
        self.db = { 
            'name' : 'cagecmf',
            'conn' : 'mongodb://localhost:27017/',
            'env' : 'testing',
        }
        self.template = 'default'
        self.static_path = None
        self.app_path = None
        self.debug = True
        self.cookie_secret = '45d1d9ed94c34749a95960db2c68c652'
        self.addons = []
        self.platform_version = '0.5.0'
        self.port = 9000
