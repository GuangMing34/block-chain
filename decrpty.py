from common import *
import base64

def decrypt_file(file_path, private_key):
    error = 'err'
    text = b''  
    max_length = int(get_max_length(private_key, False))

    with open(file_path, 'rb') as f:
        message = f.read()
    
    cipher_private = Crypto.Cipher.PKCS1_v1_5.new(private_key)
    message = base64.b64decode(message)
    while(message):
        input_data = message[:max_length]
        #update
        message = message[max_length:]
        out_data = cipher_private.decrypt(input_data, '')
        text = text + out_data
        #text += str(out_data).encode(encoding='utf-8').strip() + b"\n"
    with open(file_path, 'wb') as f:
        f.write(text)
    return True


def decrpty(blockchain, key_priv):
    ret = decrypt_file(file_need_encrpty_test, key)
    if ret:
        log.debug("decrpty pass")
    else:
        log.debug("decrypt_file fail, return")
        os._exit()


if __name__ == "__main__":
    #get bc
    blockchain = get_blockchain(blockchain_file)
    if blockchain:
        log.debug("123113")
    else:
        log.debug("get blockchain fail, return")
        os._exit()

    #id compare
    id = get_id_of_computer()
    ret = check_mac_id_in_blockchain(blockchain, id)
    if ret:
        log.debug("xxx")
    else:
        log.debug("check id fail, return")
        os._exit()
    
    #get key
    key = get_private_key_from_block(blockchain)

    if key:
        log.debug("get key pass")
    else:
        log.debug("get key fial, returm")
        os._exit()

    decrpty(blockchain, key)
    log.log_out("decrpty done")
