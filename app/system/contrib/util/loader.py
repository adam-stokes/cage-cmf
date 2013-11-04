def load_by_name(module, name):
        mod = __import__(module, fromlist=[name])
        return getattr(mod, name)
