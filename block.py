import sys
sys.dont_write_bytecode = True

import datetime
import hashlib
import json

from user import *
from transaction import *

class Block:

    def __init__(self, index, transaction_list, timestamp, previous_hash):
        self.index = index
        self.transaction_list = transaction_list
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

    def compute_hash(self):
        """
        This function wil return a hash of the block content
        """

        block_string = json.dumps(self.__dict__, default=serialize_transaction, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def __str__(self):

        str_result = "----- Block info:\n Index: {}\n previous_hash: {}\n nonce: {}\n timestamp: {}."\
                        .format(self.index, self.previous_hash, self.nonce, self.timestamp)

        return str_result
    

    def confirm_transaction(self, is_confirm=False):
        """
        This function will send coin from sender to recipient.
        """
        if is_confirm == False:
            return
        
        for transaction in self.transaction_list:
            transaction_confirmation(transaction)
