SENDGRID_API_KEY = 'REPLACE WITH SENDGRID API KEY'
FROM_EMAIL = 'REPLACE WITH VERIFIED SENDGRID EMAIL'
BASE_URL = 'http://127.0.0.1:8000'

CERTIFY_CONTRACT_ADDRESS = 'REPLACE WITH DEPLOYED CERTIFY CONTRACT ADDRESS FROM YOUR GANACHE BLOCKCHAIN'
CERTIFY_CONTRACT_ABI = '[{"anonymous": false,"inputs": [{"indexed": true,"internalType": "address","name": "owner","type": "address"},{"indexed": true,"internalType": "bytes32","name": "hash","type": "bytes32"}],"name": "DocumentAdded","type": "event"},{"inputs": [],"name": "documentCount","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function","constant": true},{"inputs": [{"internalType": "bytes32","name": "","type": "bytes32"}],"name": "documents","outputs": [{"internalType": "address","name": "owner","type": "address"},{"internalType": "bytes","name": "signature","type": "bytes"},{"internalType": "bytes","name": "publicKey","type": "bytes"},{"internalType": "bytes32","name": "hash","type": "bytes32"}],"stateMutability": "view","type": "function","constant": true},{"inputs": [{"internalType": "bytes","name": "_signature","type": "bytes"},{"internalType": "bytes","name": "_publicKey","type": "bytes"},{"internalType": "bytes32","name": "_hash","type": "bytes32"}],"name": "addDocument","outputs": [],"stateMutability": "nonpayable","type": "function"}]'
ETHEREUM_ADDRESS = 'REPLACE WITH AN ETHEREUM ADDRESS FROM YOUR GANACHE BLOCKCHAIN'

VERIFY_CONTRACT_ADDRESS = 'REPLACE WITH DEPLOYED VERIFY CONTRACT ADDRESS FROM YOUR GANACHE BLOCKCHAIN'
VERIFY_CONTRACT_ABI = '[{"inputs":[{"internalType":"address","name":"_certifyContractAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"certifyContract","outputs":[{"internalType":"contract Certify","name":"","type":"address"}],"stateMutability":"view","type":"function","constant":true},{"inputs":[{"internalType":"bytes32","name":"_hash","type":"bytes32"}],"name":"verifyDocument","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"bytes","name":"","type":"bytes"},{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function","constant":true}]'
