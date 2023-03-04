import sys
sys.dont_write_bytecode = True

from block import *
from blockchain import * 
from transaction import *
from user import *

def main():
        
    blockchain = BlockChain()

    # 0. Create user
    user_1 = User("123", "Anna", 100)
    user_2 = User("100", "Bod", 45)
    user_3 = User("999", "Cam", 300)

    blockchain.add_user(user_1)
    blockchain.add_user(user_2)
    blockchain.add_user(user_3)

    # 1. User create transaction
    tx_1 = Transaction(user_1, user_2, 10)
    tx_2 = Transaction(user_2, user_3, 20)

    # 2. Transactions are added to unconfirm pool
    blockchain.add_new_transaction(tx_1)
    blockchain.add_new_transaction(tx_2)
    
    # 3. Perform the whole mining process
    blockchain.mining_process()


    # ===== Print result =====
    # print("\n---------- Blockchain info ----------")
    # blockchain.print_chain

    print("\n---------- User account ----------")
    for user in blockchain.list_user:
        print(user, "\n")



    

main()