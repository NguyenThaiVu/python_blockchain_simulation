import hashlib
import rsa

class Transaction:
    def __init__(self, sender_private_key, sender_public_key, recipient_address, amount):
        self.sender_private_key = sender_private_key
        self.sender_public_key = sender_public_key
        self.recipient_address = recipient_address
        self.amount = amount
        
    def to_dict(self):
        return {
            'sender_public_key': self.sender_public_key.save_pkcs1().decode(),
            'recipient_address': self.recipient_address,
            'amount': self.amount
        }
    
    def sign_transaction(self):
        transaction_hash = hashlib.sha256(str(self.to_dict()).encode('utf-8')).hexdigest()
        signature = rsa.sign(transaction_hash.encode('utf-8'), self.sender_private_key, 'SHA-256')
        return signature
    
    def verify_transaction(self, signature):
        transaction_hash = hashlib.sha256(str(self.to_dict()).encode('utf-8')).hexdigest()
        try:
            rsa.verify(transaction_hash.encode('utf-8'), signature, self.sender_public_key)
            return True
        except rsa.pkcs1.VerificationError:
            return False

# Example usage
sender_private_key, sender_public_key = rsa.newkeys(512)
recipient_address = '1KZrJN8my1xNpdkFDrdMfJPNjETndzHQUb'
amount = 0.001

# Create a new transaction
transaction = Transaction(sender_private_key, sender_public_key, recipient_address, amount)

# Sign the transaction
signature = transaction.sign_transaction()

# Verify the transaction
is_valid = transaction.verify_transaction(signature)

print('Transaction:', transaction.to_dict())
print('Signature:', signature)
print('Is valid?', is_valid)
