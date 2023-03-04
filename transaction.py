import sys
sys.dont_write_bytecode = True

from user import *

class Transaction_class:

    def __init__(self, sender_public_key, recipient_address, amount_to_send):
        self.sender_public_key = sender_public_key
        self.recipient_address = recipient_address
        self.amount_to_send = amount_to_send


    def __str__(self):
        str_result = r"{} send to {} {} coins".format(self.sender.name, self.recipient.name, self.amount_to_send)
        return str_result
    
    def to_dict(self):
        return {
            'sender_public_key': self.sender_public_key.save_pkcs1().decode(),
            'recipient_address': self.recipient_address,
            'amount': self.amount_to_send
        }
    
# Define a custom serializer for the Transaction class
def serialize_transaction(transaction):
    """
    This function help json module know how to handle `Transaction` objects
    """
    if isinstance(transaction, Transaction_class):
        return {'sender': transaction.sender_public_key, 'recipient': transaction.recipient_address, 'amount_to_send': transaction.amount_to_send}
    

def transaction_confirmation(transaction, list_user):
    if isinstance(transaction, Transaction_class):
        sender_public_key = transaction.sender_public_key
        recipient_address = transaction.recipient_address
        amount_to_send = transaction.amount_to_send     # amount in the transaction

        for user in list_user:
            if user.address == recipient_address:
                user.amount_coin += amount_to_send

            if user.public_key == sender_public_key:
                user.amount_coin -= amount_to_send


    