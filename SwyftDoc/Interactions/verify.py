from web3 import Web3
from credentials import VERIFY_CONTRACT_ADDRESS, VERIFY_CONTRACT_ABI

"""
    Function to verify document 
"""
def verify_document(document_hash):
    ganache_url = "http://127.0.0.1:7545"  # Default Ganache URL
    w3 = Web3(Web3.HTTPProvider(ganache_url))

    contract_address = VERIFY_CONTRACT_ADDRESS
    contract_abi = VERIFY_CONTRACT_ABI

    # Load the contract
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    # Call the "verifyDocument" function
    owner, signature, public_key = contract.functions.verifyDocument(document_hash).call()
    return owner, signature, public_key
