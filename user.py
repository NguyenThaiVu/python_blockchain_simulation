from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import base58

class User:

    def __init__(self, id, name, amount_coin):
        self.id = id
        self.name = name
        self.amount_coin = amount_coin

        # Generate public and private key
        private_key = RSA.generate(2048)
        public_key = private_key.publickey().export_key()

        self.private_key = private_key
        self.public_key = public_key
        self.generate_address()

    def __str__(self):
        str_result = "Id: {} \nName: {} \nAmount coin: {}".format(self.id, self.name, self.amount_coin)
        return str_result
    

    def generate_address(self):
        """
        This function will generate the receiver's address.
        Which is typically derived from the receiver's public key using a hash function.
        """
        # Hash the receiver's public key with SHA256
        hash = SHA256.new(self.public_key)
        hash_bytes = hash.digest()

        address_bytes = hash_bytes[:20]

        # Add the version byte to the beginning of the address bytes
        version_byte = b'\x00'
        address_bytes = version_byte + address_bytes

        # Encode the address bytes in base58
        address = base58.b58encode(address_bytes)
        
        self.address = address