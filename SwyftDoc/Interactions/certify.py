from web3 import Web3
from credentials import CERTIFY_CONTRACT_ADDRESS, CERTIFY_CONTRACT_ABI, ETHEREUM_ADDRESS

"""
    Function to certify document 
"""
def certify_document(signature, public_key, document_hash):
    ganache_url = "http://127.0.0.1:7545"  # Default Ganache URL
    w3 = Web3(Web3.HTTPProvider(ganache_url))

    contract_address = CERTIFY_CONTRACT_ADDRESS
    contract_abi = CERTIFY_CONTRACT_ABI

    # Load the contract
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    # Ethereum account address (sender)
    eth_address = ETHEREUM_ADDRESS

    # Call the "addDocument" function
    transaction = contract.functions.addDocument(signature, public_key, document_hash)

    # Send the transaction
    transaction_hash = transaction.transact({'from': eth_address})

    # Wait for the transaction to be mined
    w3.eth.wait_for_transaction_receipt(transaction_hash)

    return transaction_hash.hex()
