from transaction import *
from user import *
from block import *
from blockchain import *


class Validator:

    def __init__(self, blockchain):
        self.unconfirmed_transactions = []
        self.blockchain = blockchain

    def verify_transaction(self, new_transaction):
        
        # Verify transaction
        transaction_info = str(new_transaction.to_dict()).encode()
        is_verified = False
        try:
            rsa.verify(transaction_info, new_transaction.signature, new_transaction.sender_public_key)
            is_verified = True                        
        except rsa.pkcs1.VerificationError:
            return False

        # If successful verify transaction, adding to unconfirm pool        
        if is_verified == True:
            self.unconfirmed_transactions.append(new_transaction)
            return True
        
        return False

    
    def proof_of_work(self, block):
        """
        In PoW, the miner must find a hash value of the block header, which meet the certain criteria.
        In PoW, miner repeatly hash the block header with difference nonce, until find the satisfy hash value.
        """

        hash_value = block.compute_hash()

        while 1:
            if hash_value.startswith('0' * self.blockchain.difficulty) == False:
                block.nonce += 1
                hash_value = block.compute_hash()
            else:
                break

        return hash_value
    

    def create_block(self):
        """
        After add transaction into unconfirmed pool. We gather some transactions into a block.
        After that, we solve the PoW puzzle.
        """
        
        current_last_block = self.blockchain.last_block

        new_block = Block(index = current_last_block.index + 1,\
                          transaction_list = self.unconfirmed_transactions,\
                          timestamp = datetime.datetime.now(),
                          previous_hash = current_last_block.compute_hash()
                        )
        
        proof = self.proof_of_work(new_block)   # result of PoW 

        return (new_block, proof)