import hashlib
import json
from time import time

def get_id_of_computer(self):
    return "test"

class Blockchain(object):
    def __init__(self):
        # block-chain data store here
        self.chain = []
        # Create the genesis block
        self.new_block(previous_hash = 0, proof = 100)
    def new_block(self, proof, previous_hash=None):
        """
        Éú³ÉÐÂ¿é
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.chain.append(block)
        return block

    @property
    def last_block(self):
        return self.chain[-1]
    @staticmethod
    def hash(block):
        if 'get_id_of_computer' in dir():
            block_string = get_id_of_computer()
        else:
            print("get_id_of_computer is not in dir, dir:" + dir())
            block_string = "test"
        return hashlib.sha256(block_string).hexdigest() 
