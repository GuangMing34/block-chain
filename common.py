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
file_need_encrpty_test = "./test_file/test1.txt"
blockchain_file = "./blockchain.txt"
encrpty_step = 20
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
def create_genesis_block(id):
    return MyBlock(0, time(), get_id_of_computer(), id)

## get next block by last block
def next_block(last_block, mac_id):
    this_index = str(int(last_block.index) + 1)
    this_timestamp = time()
    this_id = mac_id
    this_hash = last_block.hash
    return MyBlock(this_index, this_timestamp, this_id, this_hash)


def block_member_print(block):
    log.log_raw("index, timestamp, id, previous_hash, hash==========>")
    log.log_raw(block.index)
    log.log_raw(block.timestamp)
    log.log_raw(block.id)
    log.log_raw(block.previous_hash)
    log.log_raw(block.hash)
    log.log_raw("<==========index, timestamp, id, previous_hash, hash")

def block_chain_check(blockchain, block_size):
    i = 0
    if block_size == 1:
        return True

    for block in blockchain:
        if(block.hash != blockchain[i + 1].previous_hash):
            log.log_out("check fail")
            return False

        if i >= (block_size - 2):
            break
        i = i + 1

    log.debug("check pass")
    return True


def get_hash_legth():
    block = MyBlock(0, time(), get_id_of_computer())
    return len(block.hash)


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


def check_mac_id_in_blockchain(blockchain ,mac_id):
    i = 0
    for block in blockchain:
        log.debug("id  mac_id")
        log.log_raw(blockchain[i].id)
        log.log_raw(mac_id)
    
        if blockchain[i].id == mac_id:
            log.debug("check %d times" %i)
            return True
        i += 1

    return False

def save_blockchain(blockchain, block_size):
    i = 0
    with open(blockchain_file, 'w') as f:
        f.write(str(block_size) + '\n')
        for block in blockchain:
            if i == 0:
                ## add one blank line
                f.write(str(block.previous_hash) + '\n' + '\n')

                f.write(str(block.index) + '\n')
                f.write(str(block.timestamp) + '\n')
                f.write(str(block.id) + '\n')
                f.write(str(block.hash) + '\n')
            else:
                f.write(str(block.index) + '\n')
                f.write(str(block.timestamp) + '\n')
                f.write(str(block.id) + '\n')
                f.write(str(block.previous_hash) + '\n')
                f.write(str(block.hash) + '\n')
            i = i + 1

def get_blockchain(blockchain_file):
    blockchain = []
    if os.path.exists(blockchain_file) is not True:
        log.debug("does not exist file, exit")
        return False

    with open(blockchain_file, 'r') as f:
        blockchain_size = f.readline()
        priv = ''
        for i in range(0, int(blockchain_size)):
            block = create_genesis_block("0")
            if i == 0:
                while True:
                    current_line = f.readline()
                    if current_line != "\n":
                        priv = priv + current_line
                    else:
                        break
                block.previous_hash = priv
                block.index = f.readline().split("\n")[0]
                block.timestamp = f.readline().split("\n")[0]
                block.id = f.readline().split("\n")[0]
                block.hash = f.readline().split("\n")[0]
            else:
                block.index = f.readline().split("\n")[0]
                block.timestamp = f.readline().split("\n")[0]
                block.id = f.readline().split("\n")[0]
                block.previous_hash = f.readline().split("\n")[0]
                block.hash = f.readline().split("\n")[0]
            blockchain.append(block)
    return blockchain
    
def get_private_key_from_block(blockchain):
    key_raw = blockchain[0].previous_hash
    key = RSA.importKey(key_raw)
    return key

def get_max_length(rsa_key, encrypt=True):
    blocksize = Crypto.Util.number.size(rsa_key.n) / 8
    reserve_size = 11
    if not encrypt:
        reserve_size = 0
    maxlength = blocksize - reserve_size
    return maxlength