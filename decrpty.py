#system lib
from time import time
import fileinput
import os

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
blockchain_file = "./blockchain.txt"

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
def next_block(last_block, mac_id):
    this_index = mac_id
    this_timestamp = time()
    this_id = get_id_of_computer()
    this_hash = last_block.hash
    return MyBlock(this_index, this_timestamp, this_id, this_hash)

def get_block_id(block):
    return block.id


def block_chain_check(blockchain, block_size):
    i = 0
    for block in blockchain:      
        if(block.hash != blockchain[i + 1].previous_hash):
            log.log_out("check fail")
            return False
        i = i + 1
        if i == (block_size - 2):
            break

    log.debug("check pass")
    return True


def get_hash_legth():
    block = MyBlock(0, time(), get_id_of_computer())
    return len(block.hash)

####file encrypt part
def encrpty_file(file_path, pubkey):

    log.debug("+++++++")
    with open(file_path, 'rb') as f:
        message = f.read()
        log.log_raw(message)
    
    log.debug("-------")
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

def decrypt_file(file_path, private_key):
    with open(file_path, 'rb') as f:
        message = f.read()
        log.log_raw(message)

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
        return False

    return True


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
            block_to_add = next_block(previous_block, mac_id)
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
                log.debug(blockchain[i].previous_hash)
                log.debug("Hash: %s\n" %format(blockchain[i].hash))
            break
    ## block chain check
    check = block_chain_check(blockchain, blockchain_len)
    if check:
        pubkey = get_key.get_public_key()
        encrpty_file(file_need_encrpty_test, pubkey)
        log.log_out("file encrpty done!" + file_need_encrpty_test)
    else:
        log.debug("check fail")
        return False


def get_blockchain(blockchain_file):
    blockchain = []
    if os.path.exists(blockchain_file):
        log.debug("file exist")
    else:
        log.debug("does not exist file, exit")
        return False

    with open(blockchain_file, 'r') as f:
        blockchain_size = f.readline()
        block = create_genesis_block(0)
        for i in range(0, int(blockchain_size)):
            '''
            f.write(str(block.index) + '\n')
            f.write(str(block.timestamp) + '\n')
            f.write(str(block.id) + '\n')
            f.write(str(block.previous_hash) + '\n')
            f.write(str(block.hash) + '\n')
            '''

            block.index = f.readline().split("\n")[0]
            block.timestamp = f.readline().split("\n")[0]
            block.id = f.readline().split("\n")[0]
            block.previous_hash = f.readline().split("\n")[0]
            block.hash = f.readline().split("\n")[0]
            blockchain.append(block)
    return blockchain

def check_mac_id_in_blockchain(blockchain ,mac_id):
    i = 0
    for block in blockchain:
        i += 1
        log.debug("id  mac_id")
        log.log_raw(block.id)
        log.log_raw(mac_id)
    
        if block.id == mac_id:
            print("check %d times" %i)
            return True

    print("check %d times" %i)
    return False
    
def get_private_key_from_block(blockchain):
    return blockchain[0].id


if __name__ == "__main__":
    # execute only if run as a script
    id = get_id_of_computer()
    blockchain = get_blockchain(blockchain_file)
    if blockchain:
        log.debug("get blockchain pass")
    else:
        log.debug("get blockchain fail, return")
        os._exit()
    
    ret = check_mac_id_in_blockchain(blockchain, id)
    if ret:
        log.debug("check id pass")
    else:
        log.debug("check id fail, return")
        os._exit()
    
    key = get_private_key_from_block(blockchain)

    if key:
        log.debug("get key pass")
    else:
        log.debug("get key fial, returm")
        os._exit()
    
    ret = decrypt_file(file_need_encrpty_test , key)
    if ret:
        log.debug("decrpty pass")
    else:
        log.debug("decrypt_file fail, return")
        os._exit()
