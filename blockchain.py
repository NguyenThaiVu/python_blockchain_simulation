"""
This script is get from https://www.geeksforgeeks.org/create-simple-blockchain-using-python/
"""

import sys
sys.dont_write_bytecode = True
import datetime
import hashlib

from block import *
from user import *
from transaction import *
from validator import *
    

class BlockChain:

    def __init__(self, difficulty = 2):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()
        
        self.list_user = set()


    def create_genesis_block(self):
        genesis_block = Block(0, [], datetime.datetime.now(), "0")
        self.chain.append(genesis_block)


    @property
    def last_block(self):
        return self.chain[-1]


    def add_validator(self, validator:Validator):
        self.validator = validator


    def broadcast_transaction(self, new_transaction):
        """
        When the blockchain network receive the transaction, it will broadcast transaction to the validator
        """

        if self.validator.verify_transaction(new_transaction) == False:
            print("[ERROR] Can not verify transaction: {}",format(new_transaction))


    def is_valid_proof(self, block, PoW_result):
        """
        Check if block_hash is valid hash of block and satisfies the difficulty criteria.
        """    

        return (PoW_result.startswith('0' * self.difficulty) == True)\
                & (PoW_result == block.compute_hash())
    

    def add_block(self, block, proof):
        """
        In this function, before adding a new block, we need to verify this block.
        - Check if the `previous_hash` of this block and the hash value of the lastest block is match.
        - Check if the proof is valid.
        """

        if self.last_block.compute_hash() != block.previous_hash:
            return False
        
        if self.is_valid_proof(block, proof) == False:
            return False
        
        self.chain.append(block)
        return True
            
    
    def mining_process(self):
        """
        This function perform:
        - Validator create a new block.
        - Add block to blockchain
        """
       
        (new_block, proof) = self.validator.create_block()
        
        is_add_block_success = self.add_block(new_block, proof)

        if is_add_block_success == True:
            self.validator.unconfirmed_transactions = []
            print("[INFO] Successfully add new block.")

            new_block.confirm_transaction(self.list_user, is_confirm=True)
        else:
            print("[ERROR] Add new block to chain fail") 


    def print_chain(self):

        num_blocks = self.chain[-1].index
        print("Number of blocks: {}".format(num_blocks))
        
        for i in range(num_blocks):
            print(self.chain[i])
   

    def add_user(self, new_user):
        self.list_user.add(new_user)
