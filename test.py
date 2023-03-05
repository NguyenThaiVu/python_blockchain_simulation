import json
import rsa
import hashlib
import base58

def generate_address(public_key):
        """
        This function will generate the receiver's address.
        Which is typically derived from the receiver's public key using a hash function.
        """
        
        public_key_der = rsa.PublicKey.save_pkcs1(public_key, format='DER')    # Convert the public key to DER format
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
        
        return address.decode()

def save_user_to_json(id, name, amount_coin, private_key, public_key, address):
    user_data = {
                    'id': id,\
                    'name': name,\
                    'amount_coin': amount_coin,\
                    'private_key': private_key,\
                    'public_key': public_key,\
                    'address': address                  
                }

    filename = r'user/{id}.json'
    
    with open(filename, 'w') as f:
        json.dump(user_data, f)

# Example usage
id = '100'
name = 'Alice'
amount_coin = 100
public_key, private_key = rsa.newkeys(512)
address = generate_address(public_key)

save_user_to_json(id, name, amount_coin, private_key, public_key, address)