import pickle as pkl
from bson.json_util import dumps
from app.system.encryption import encrypt, decrypt

def pkl_secure(obj_to_pickle, key):
    pickle_str = pkl.dumps(obj_to_pickle)
    encoded_str = encrypt(key, pickle_str)
    return encoded_str

def pkl_decode_secure(encoded_str, key):
    pickle_str = decrypt(key, encoded_str)
    pickle_obj = pkl.loads(pickle_str)
    return pickle_obj

def to_json(entity):
    """ converts object to json """
    if type(entity) is str:
        return dumps(entity, sort_keys=True, indent=4)
    else:
        return dumps(entity.__dict__, sort_keys=True, indent=4)

