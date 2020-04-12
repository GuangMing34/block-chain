#system lib
from time import time
import fileinput

#hash lib
import hashlib as hasher

## encrpty lib
from Crypto.Hash import SHA256, SHA, SHA512
from Crypto.PublicKey import RSA
import Crypto.Cipher.PKCS1_v1_5
import Crypto.Random
import Crypto.Signature.PKCS1_v1_5
import rsa

## project lib
import get_key
import my_log as log


## windows 
import win32api,win32con

###global variable
file_need_encrpty = "./test_file/test1.docx"
file_need_encrpty_test = "./test_file/test1.txt"

'''
Todo:
### history data
    record any history

'''

## get mac id
def get_id_of_computer():
    import uuid
    node = uuid.getnode()
    mac = uuid.UUID(int = node).hex[-12:]
    return mac

# class define, for generate block unit
class MyBlock:
    def __init__(self, index, timestamp, id, previous_hash = "0"):
        self.index = index
        self.timestamp = time()
        self.id = id
        self.previous_hash = previous_hash #previous hash value
        need_hash = (str(index) + str(timestamp) + str(id) + str(previous_hash)).encode("utf-8")
        self.hash = self.hash_block(need_hash) # current node hash value

    @staticmethod
    def hash_block(need_hash):
        h = SHA256.new()
        h.update(need_hash)
        return h.hexdigest()


# Manually construct a block with
# index zero and arbitrary previous hash
def create_genesis_block(key):
    return MyBlock(0, time(), get_id_of_computer(), key)

## get next block by last block
def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = time()
    this_id = get_id_of_computer()
    this_hash = last_block.hash
    return MyBlock(this_index, this_timestamp, this_id, this_hash)

def get_block_id(block):
    return block.id

def block_chain_check(blockchain, block_size):
    i = 0
    for block in blockchain:
        if(MyBlock.hash_block(blockchain[i + 1].previous_hash) != block.hash):
            return False
        i = i + 1

    return True

def get_hash_legth():
    block = MyBlock(0, time(), get_id_of_computer())
    return len(block.hash)

####file encrypt part
def encrpty_file(file_path):

    log.debug("+++++++")
    with open(file_path, 'rb') as f:
        message = f.read()
        log.log_raw(message)
    
    log.debug("-------")
    pubkey = get_key.get_public_key()
    if pubkey:
        cipher_public = Crypto.Cipher.PKCS1_v1_5.new(pubkey)
        cipher_text = cipher_public.encrypt(message)
        # update file
        with open(file_path, 'wb') as f:
            f.write(cipher_text)

        with open(file_path, 'rb') as f:
            message = f.read()
            log.log_raw(message)
    else:
        win32api.MessageBox(0, "error", "Error",win32con.MB_ICONWARNING)
        return

####file decrypt part

def decrypt_file(file_path):
    with open(file_path, 'rb') as f:
        message = f.read()
        log.log_raw(message)

    private_key = get_key.get_private_key()
    if private_key:
        cipher_private = Crypto.Cipher.PKCS1_v1_5.new(private_key)
        err = ""
        text = cipher_private.decrypt(message, err)
        log.debug("after=======>")
        log.log_raw(text)
        log.debug("=======>")
        log.log_raw(err)
        with open(file_path, 'wb') as f:
            f.write(text)
    else:
        win32api.MessageBox(0, "No permission", "Error",win32con.MB_ICONWARNING)


def read_and_print_file():
    hash_len = get_hash_legth()
    #hash_len = 10
    total_len = 0

    with open(file_need_encrpty_test,'rb') as f:
        log.debug("file open success:" + file_need_encrpty_test)
    #with open(file_need_encrpty,'rb') as f:
        words = f.read(10)
        while 1:
            log.log_str(words)
            if (len(words) == 10):
                total_len = total_len + 10
                words = f.read(10)
                continue
            else:
                total_len = total_len + len(words)
                log.debug("len :" + str(len(words)))
                log.debug("total len:" + str(total_len))
                break

###start
# Create the blockchain and add the genesis block
def block_chain_flow():
    private_key = get_key.get_private_key()
    ## store key @ block 0
    blockchain = [create_genesis_block(str(private_key))]
    previous_block = blockchain[0]
    blockchain_len = 1;

    log.debug(previous_block.hash + '\n' + previous_block.id)
    log.debug(previous_block.previous_hash)

    a = input("are you want to add another device? y :yes  n :No:")
    while True:
        if (a == 'y'):
            mac_id = input("input your mac_id, please input numbers only")
            if (mac_id == 'y' or mac_id == 'Y'):
                block_to_add = next_block(previous_block)
                blockchain.append(block_to_add)
                previous_block = block_to_add
                blockchain_len = blockchain_len + 1
                print(blockchain_len)
            a = input("are you want to add another device? y :yes  n :No:")
        else:
            log.log_out("add done，blocks below:")
            log.log_out(blockchain_len)
            for i in range(0, blockchain_len):
                log.debug("Block %s has been added to the blockchain!" %format(blockchain[i].index))
                log.debug("Hash: %s\n" %format(blockchain[i].hash))
            break
    ## block chain check
    block_chain_check(blockchain, blockchain_len)



if __name__ == "__main__":
    # execute only if run as a script
    block_chain_flow()
    #read_and_print_file()