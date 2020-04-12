from time import time

#hash lib
import hashlib as hasher

## encrpty lib
#from Crypto.Hash import SHA256, SHA, SHA512


###global variable
file_need_encrpty = "./test_file/test1.docx"
file_need_encrpty_test = "./test_file/test1.txt"


'''
Todo:
### history data
    record any history

'''

def my_print(x):
    print(x)

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
def create_genesis_block():
    return MyBlock(0, time(), get_id_of_computer(), "0")

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
def read_and_print_file():
    #hash_len = get_hash_legth()
    hash_len = 10
    total_len = 0

    with open(file_need_encrpty_test,'rb') as f:
        print("file open success:" + file_need_encrpty_test)
    #with open(file_need_encrpty,'rb') as f:
        words = f.read(10)
        while 1:
            my_print(words)
            if (len(words) == 10):
                total_len = total_len + 10
                words = f.read(10)
                continue
            else:
                total_len = total_len + len(words)
                print("len :" + str(len(words)))
                print("total len:" + str(total_len))
                break;



###start
# Create the blockchain and add the genesis block
def block_chain_flow():
    blockchain = [create_genesis_block()]
    previous_block = blockchain[0]

    print(previous_block.hash + '\n' + previous_block.id)

    # How many blocks should we add to the chain
    # after the genesis block
    num_of_blocks_to_add = 20

    # Add blocks to the chain
    for i in range(0, num_of_blocks_to_add):
        block_to_add = next_block(previous_block)
        blockchain.append(block_to_add)
        previous_block = block_to_add
        # Tell everyone about it!
        print("Block %s has been added to the blockchain!" %format(block_to_add.index))
        print("Hash: %s\n" %format(block_to_add.hash))

    ## block chain check
    block_chain_check(blockchain, num_of_blocks_to_add)



if __name__ == "__main__":
    # execute only if run as a script
    #block_chain_flow()
    read_and_print_file()