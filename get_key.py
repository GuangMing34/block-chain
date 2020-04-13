from Crypto.PublicKey import RSA
import os
import my_log as log

PublicKey_path = "./public.pem"
PrivateKey_path = "D:/mykey.pem"

def get_private_key():
    # public key
    if os.path.exists(PrivateKey_path):
        log.debug("exist private key")
        with open(PrivateKey_path, 'r') as f:
            key_raw = f.read()
        key = RSA.importKey(key_raw)
        #log.log_raw(key)
        return key
    else :
        log.debug("doesn't exist private key!!!!")
        return False

def get_private_key_bytes():
    # public key
    if os.path.exists(PrivateKey_path):
        with open(PrivateKey_path, 'rb') as f:
            key_raw = f.read()
        log.debug(key_raw)
        log.debug(type(key_raw))
        return key_raw
    else :
        log.debug("doesn't exist private key!!!!")
        return False

def get_private_key_strs():
    # public key
    if os.path.exists(PrivateKey_path):
        with open(PrivateKey_path, 'r') as f:
            key_raw = f.read()
        return key_raw
    else :
        log.debug("doesn't exist private key!!!!")
        return False

def get_public_key():
    # public key
    if os.path.exists(PublicKey_path):
        with open(PublicKey_path, 'r') as f:
            key_raw = f.read()
        key = RSA.importKey(key_raw)
        log.log_raw(key)
        return key
    else :
        log.debug("doesn't exist public key!!!!")
        return False

def get_public_key_str():
    # public key
    if os.path.exists(PublicKey_path):
        log.debug("exist public key")
        with open(PublicKey_path, 'r') as f:
            key_raw = f.read()
        #log.log_raw(key_raw)
        return key_raw
    else :
        log.debug("doesn't exist public key!!!!")
        return False

'''
get_public_key()
get_private_key()
get_private_key_str()
get_public_key_str()
'''
