from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    print(simple_storage_file)

# Compile Our Solidity Contract
install_solc("0.6.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode, this is walking down the json tree to access the bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connect to the loclal blockchain from Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
# chain or network id
chain_id = 1337
# set the address of the account that will deploy the contract
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
# set the private key of the account that will deploy the contract
private_key = os.getenv("PRIVATE_KEY")

# create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# get the latest nonce(transaction count)
nonce = w3.eth.getTransactionCount(my_address)

# 1. Build the transaction
# 2. Sign the transaction
# 3. Send the transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

signed_txn = w3.eth.account.signTransaction(transaction, private_key)

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


# Work with the contract
# 1. Get the contract address
# 2. Get the contract abi
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# to interact with the contract, we can:
#        Call -> Simulates making the call and getting the return value
#        Transact -> Actually makes a state change
print(simple_storage.functions.retrieve().call())
store_transaction = simple_storage.functions.store(42).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)

signed_store_txn = w3.eth.account.signTransaction(
    store_transaction, private_key=private_key
)
transaction_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

print(simple_storage.functions.retrieve().call())
