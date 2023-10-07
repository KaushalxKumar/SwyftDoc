from web3 import Web3

"""
    Function to certify document 
"""
def certify_document(signature, public_key, document_hash):
    ganache_url = "http://127.0.0.1:7545"  # Default Ganache URL
    w3 = Web3(Web3.HTTPProvider(ganache_url))

    # SwyftDoc
    # contract_address = "0x1f4e74Db89C830E2986c6A30607E41a884f18eB3"

    # SwyftDoc +
    contract_address = '0x917EF4417489180621c5220DE2B87A3eabFa9E65'

    contract_abi = '[{"anonymous": false,"inputs": [{"indexed": true,"internalType": "address","name": "owner","type": "address"},{"indexed": true,"internalType": "bytes32","name": "hash","type": "bytes32"}],"name": "DocumentAdded","type": "event"},{"inputs": [],"name": "documentCount","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function","constant": true},{"inputs": [{"internalType": "bytes32","name": "","type": "bytes32"}],"name": "documents","outputs": [{"internalType": "address","name": "owner","type": "address"},{"internalType": "bytes","name": "signature","type": "bytes"},{"internalType": "bytes","name": "publicKey","type": "bytes"},{"internalType": "bytes32","name": "hash","type": "bytes32"}],"stateMutability": "view","type": "function","constant": true},{"inputs": [{"internalType": "bytes","name": "_signature","type": "bytes"},{"internalType": "bytes","name": "_publicKey","type": "bytes"},{"internalType": "bytes32","name": "_hash","type": "bytes32"}],"name": "addDocument","outputs": [],"stateMutability": "nonpayable","type": "function"}]'

    # Load the contract
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    # Ethereum account address (sender)
    # SwyftDoc
    # eth_address = "0xF79fA568E7CA0f164C4e0A825facDD89fb50dC08"

    # SwyftDoc+
    eth_address = '0x7aF240B73746B78F334dF38cBc9f02F94a6E378C'

    # Call the "addDocument" function
    transaction = contract.functions.addDocument(signature, public_key, document_hash)

    # Send the transaction
    transaction_hash = transaction.transact({'from': eth_address})

    # Wait for the transaction to be mined
    w3.eth.wait_for_transaction_receipt(transaction_hash)

    return transaction_hash.hex()



#
# def certify_document(signature, public_key, document_hash):
#     ganache_url = "http://127.0.0.1:7545"  # Default Ganache URL
#     w3 = Web3(Web3.HTTPProvider(ganache_url))
#
#     contract_address = "0x1f4e74Db89C830E2986c6A30607E41a884f18eB3"
#     contract_abi = '[{"anonymous": false,"inputs": [{"indexed": true,"internalType": "address","name": "owner","type": "address"},{"indexed": true,"internalType": "bytes32","name": "hash","type": "bytes32"}],"name": "DocumentAdded","type": "event"},{"inputs": [],"name": "documentCount","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function","constant": true},{"inputs": [{"internalType": "bytes32","name": "","type": "bytes32"}],"name": "documents","outputs": [{"internalType": "address","name": "owner","type": "address"},{"internalType": "bytes","name": "signature","type": "bytes"},{"internalType": "bytes","name": "publicKey","type": "bytes"},{"internalType": "bytes32","name": "hash","type": "bytes32"}],"stateMutability": "view","type": "function","constant": true},{"inputs": [{"internalType": "bytes","name": "_signature","type": "bytes"},{"internalType": "bytes","name": "_publicKey","type": "bytes"},{"internalType": "bytes32","name": "_hash","type": "bytes32"}],"name": "addDocument","outputs": [],"stateMutability": "nonpayable","type": "function"}]'
#
#     # Load the contract
#     contract = w3.eth.contract(address=contract_address, abi=contract_abi)
#
#     # Ethereum account address (sender)
#     eth_address = "0xF79fA568E7CA0f164C4e0A825facDD89fb50dC08"
#
#     # Call the "addDocument" function
#     transaction = contract.functions.addDocument(signature, public_key, document_hash)
#
#     # Create a transaction dictionary
#     transaction_dict = {
#         'to': contract.address,
#         'data': transaction.buildTransaction({'chainId': 1})['data'],  # Include the contract function data
#         'gas': 2000000,  # Set the gas limit as needed
#         'gasPrice': w3.toWei('20', 'gwei'),  # Set the gas price as desired
#         'nonce': w3.eth.getTransactionCount(eth_address),
#     }
#
#     # Send the transaction
#     transaction_hash = transaction.transact({'from': eth_address})
#
#     # Wait for the transaction to be mined
#     w3.eth.wait_for_transaction_receipt(transaction_hash)
#
#     return transaction_hash.hex()
