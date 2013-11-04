import base64
import urllib
import Crypto.Cipher.AES as AES

def encrypt(key, decrypted_str):
    encryptor = AES.new(key[0:16])
    # Pad the string to be multiple of 16
    decrypted_str += ' ' * (16 - len(decrypted_str) % 16)
    encrypted_str = encryptor.encrypt(decrypted_str)

    # encode str
    encoded_str = urllib.parse.quote(base64.b64encode(encrypted_str).replace("/",".").replace("+","_").replace("=","-"))
    return encoded_str


def decrypt(key, quoted_str):
    decryptor = AES.new(key[0:16])
    encoded_str = urllib.parse.unquote(quoted_str)
    encrypted_str = base64.b64decode(encoded_str.replace(".","/").replace("_","+").replace("-","="))
    decrypted_str = decryptor.decrypt(encrypted_str).strip()
    return decrypted_str
