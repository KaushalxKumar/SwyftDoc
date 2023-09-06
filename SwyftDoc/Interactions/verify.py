from web3 import Web3

def verify_document(document_hash):
    ganache_url = "http://127.0.0.1:7545"  # Default Ganache URL
    w3 = Web3(Web3.HTTPProvider(ganache_url))

    contract_address = "0xC8aB0fEddE5edD8d7044d7B5A2664F25d52eacD3"
    contract_abi = '[{"inputs":[{"internalType":"address","name":"_certifyContractAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"certifyContract","outputs":[{"internalType":"contract Certify","name":"","type":"address"}],"stateMutability":"view","type":"function","constant":true},{"inputs":[{"internalType":"bytes32","name":"_hash","type":"bytes32"}],"name":"verifyDocument","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"bytes","name":"","type":"bytes"},{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function","constant":true}]'

    # Load the contract
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    # Call the "verifyDocument" function
    owner, signature, public_key = contract.functions.verifyDocument(document_hash).call()
    return owner, signature, public_key

