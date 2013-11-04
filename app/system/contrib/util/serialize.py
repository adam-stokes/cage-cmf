import pickle as pkl
from app.system.contrib.encryption import encrypt, decrypt

def pkl_secure(obj_to_pickle, key):
    pickle_str = pkl.dumps(obj_to_pickle)
    encoded_str = encrypt(key, pickle_str)
    return encoded_str

def pkl_decode_secure(encoded_str, key):
    pickle_str = decrypt(key, encoded_str)
    pickle_obj = pkl.loads(pickle_str)
    return pickle_obj
    
def return_json_response(handler, content):
    handler.set_header("Content-Type", "application/json")
    if ("callback" in handler.request.arguments):
        handler.write('%s(%s)' % (handler.get_argument('callback'), content))
    else:
        handler.write(content)
