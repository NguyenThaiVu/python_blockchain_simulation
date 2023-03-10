import sys
sys.dont_write_bytecode = True

from block import *
from blockchain import *
from transaction import *
from user import *
from validator import *

def main():
        
    blockchain = BlockChain()
    validator = Validator(blockchain)
    blockchain.add_validator(validator)

    # 0. Create user
    user_1 = User("123", "Anna", 100)
    user_2 = User("100", "Bod", 200)
    user_3 = User("999", "Cam", 300)

    blockchain.add_user(user_1)
    blockchain.add_user(user_2)
    blockchain.add_user(user_3)

    # 1. User create transaction
    new_transaction_1 = user_1.create_transaction(user_2.address, 10)
    new_transaction_2 = user_2.create_transaction(user_3.address, 20)


    # 2. Transactions are added to unconfirm pool
    blockchain.broadcast_transaction(new_transaction_1)
    blockchain.broadcast_transaction(new_transaction_2)
    

    # 3. Perform the whole mining process
    blockchain.mining_process()


    # ===== Print result =====
    # print("\n---------- Blockchain info ----------")
    # blockchain.print_chain()

    print("\n---------- User account ----------")
    for user in blockchain.list_user:
        print(user, "\n")

    

main()