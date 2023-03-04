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
    

class BlockChain:

    def __init__(self, difficulty = 2):
        self.unconfirmed_transactions = []
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


    def proof_of_work(self, block):
        """
        In PoW, the miner must find a hash value of the block header, which meet the certain criteria.
        In PoW, miner repeatly hash the block header with difference nonce, until find the satisfy hash value.
        """

        hash_value = block.compute_hash()

        while 1:
            if hash_value.startswith('0' * self.difficulty) == False:
                block.nonce += 1
                hash_value = block.compute_hash()
            else:
                break

        return hash_value


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
        

    def verify_transaction(self, transaction):
        transaction_info = str(transaction.to_dict()).encode()
        try:
            rsa.verify(transaction_info, transaction.signature, transaction.sender_public_key)
            return True
        except rsa.pkcs1.VerificationError:
            return False

    def add_new_transaction(self, new_transaction):
        if self.verify_transaction(new_transaction) == True:
            self.unconfirmed_transactions.append(new_transaction)
        else:
            print("[ERROR] Transaction is not verified")
 
    
    def mining_process(self):
        """
        This function perform:
        - Gather list of unconfirm transaction into block.
        - Solve PoW.
        - Add block to blockchain
        """

        current_last_block = self.last_block

        new_block = Block(index = current_last_block.index + 1,\
                          transaction_list = self.unconfirmed_transactions,\
                          timestamp = datetime.datetime.now(),
                          previous_hash = current_last_block.compute_hash()
                        )
        
        proof = self.proof_of_work(new_block)   # result of PoW 
        
        is_add_block_success = self.add_block(new_block, proof)

        if is_add_block_success == True:
            self.unconfirmed_transactions = []
            print("[INFO] Successfully add new block.")

            new_block.confirm_transaction(self.list_user, is_confirm=True)
        else:
            print("[ERROR] Add new block to chain fail") 


    @property
    def print_chain(self):

        num_blocks = self.chain[-1].index
        print("Number of blocks: {}".format(num_blocks))
        
        for i in range(num_blocks):
            print(self.chain[i])
   

    def add_user(self, new_user):
        self.list_user.add(new_user)
