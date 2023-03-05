import base58
import hashlib
import rsa

from transaction import *

class User:

    def __init__(self, id, name, amount_coin):
        self.id = id
        self.name = name
        self.amount_coin = amount_coin

        # Generate public key and private key
        public_key, private_key = rsa.newkeys(512)
        self.private_key = private_key
        self.public_key = public_key

        self.generate_address()

    def __str__(self):
        str_result = "Name: {} \nAmount coin: {}".format(self.name, self.amount_coin)
        return str_result
    

    def generate_address(self):
        """
        This function will generate the receiver's address.
        Which is typically derived from the receiver's public key using a hash function.
        """
        
        public_key_der = rsa.PublicKey.save_pkcs1(self.public_key, format='DER')    # Convert the public key to DER format
        hash = hashlib.sha256(public_key_der).digest()    # Hash the public key using SHA-256
        
        # Hash the result again using RIPEMD-160
        ripe_md160 = hashlib.new('ripemd160')
        ripe_md160.update(hash)
        hash = ripe_md160.digest()
        
        # Add a network byte (0x00 for mainnet, 0x6f for testnet)
        network_byte = b'\x00'
        hash_with_network_byte = network_byte + hash
        
        # Compute the checksum by hashing the hash_with_network_byte twice and taking the first 4 bytes
        checksum = hashlib.sha256(hashlib.sha256(hash_with_network_byte).digest()).digest()[:4]
        
        address_bytes = hash_with_network_byte + checksum        
        address = base58.b58encode(address_bytes)
        
        self.address = address.decode()


    def sign_transaction(self, transaction):
        """
        This method use the sender's private key to sign the transaction data and generate a signature.
        """
        transaction_info = str(transaction.to_dict()).encode()
        signature = rsa.sign(transaction_info, self.private_key, 'SHA-256')
        
        transaction.signature = signature


    def create_transaction(self, recipient_address, amount_to_send):

        new_transaction = Transaction_class(self.public_key, recipient_address, amount_to_send)
        self.sign_transaction(new_transaction)

        return new_transaction