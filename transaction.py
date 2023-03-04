import sys
sys.dont_write_bytecode = True

from user import *

class Transaction:

    def __init__(self, sender, recipient_address, amount):
        self.sender = sender
        self.recipient_address = recipient_address
        self.amount = amount

    def __str__(self):
        str_result = r"{} send to {} {} coins".format(self.sender.name, self.recipient.name, self.amount)
        return str_result
    
# Define a custom serializer for the Transaction class
def serialize_transaction(transaction):
    """
    This function help json module know how to handle `Transaction` objects
    """
    if isinstance(transaction, Transaction):
        return {'sender': transaction.sender, 'recipient': transaction.recipient, 'amount': transaction.amount}
    

def transaction_confirmation(transaction):
    if isinstance(transaction, Transaction):
        sender = transaction.sender
        recipient = transaction.recipient
        amount = transaction.amount     # amount in the transaction

        sender.amount_coin -= amount
        recipient.amount_coin += amount
