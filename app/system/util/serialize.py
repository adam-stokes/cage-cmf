import pickle as pkl
from app.system.encryption import encrypt, decrypt

def pkl_secure(obj_to_pickle, key):
    pickle_str = pkl.dumps(obj_to_pickle)
    encoded_str = encrypt(key, pickle_str)
    return encoded_str

def pkl_decode_secure(encoded_str, key):
    pickle_str = decrypt(key, encoded_str)
    pickle_obj = pkl.loads(pickle_str)
    return pickle_obj
