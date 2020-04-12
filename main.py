from time import time

#hash lib
import hashlib as hasher

## encrpty lib
from Crypto.Hash import SHA256, SHA, SHA512


###global variable
file_need_encrpty = "./test_file/test1.docx"
file_need_encrpty_test = "./test_file/test1."


'''
Todo:
### history data
    record any history

'''


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
    return MyBlock(0, time(), get_id_of_computer())

## get next block by last block
def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = time()
    this_id = get_id_of_computer()
    this_hash = last_block.hash
    return MyBlock(this_index, this_timestamp, this_id, this_hash)




####file encrypt part
def read_and_print_file():
    with open(file_need_encrpty_test,'rb') as f:
        print("file open success:" + file_need_encrpty_test)
    #with open(file_need_encrpty,'rb') as f:
        words = f.read(10)
        if (words):
            print(words)
        else:
            print("None")



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



if __name__ == "__main__":
    # execute only if run as a script
    #block_chain_flow()
    read_and_print_file()