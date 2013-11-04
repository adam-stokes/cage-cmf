import urllib
import base64
import re
import unicodedata

def hash_login(username, password):
    str_to_hash = "@@@@%s%s@@@@" % (username, password)
    b64encode = urllib.quote(base64.b64encode(str_to_hash).replace("/",".").replace("+","_").replace("=","-"))
    return b64encode

# text utilities
def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    http://code.djangoproject.com/svn/django/trunk/django/template/defaultfilters.py
    """
    value = unicode(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)

def get_dict_from_sequence(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))
