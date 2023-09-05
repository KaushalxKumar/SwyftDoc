pragma solidity 0.8.0;

contract Certify {
    struct Document {
        address owner;       // Address of the document owner
        bytes signature;     // EdDSA signature of the document
        bytes publicKey;     // Public key of the document
        bytes32 hash;        // Hash of the document data
    }

    mapping(bytes32 => Document) public documents;
    uint256 public documentCount;

    // Event to log when a new document is added
    event DocumentAdded(address indexed owner, bytes32 indexed hash);

    // Function to add a new document
    function addDocument(bytes memory _signature, bytes memory _publicKey, bytes32 _hash) public {
        require(documents[_hash].owner == address(0), "Document with this hash already exists");

        documents[_hash] = Document({
            owner: msg.sender,
            signature: _signature,
            publicKey: _publicKey,
            hash: _hash
        });

        emit DocumentAdded(msg.sender, _hash);
        documentCount++;
    }
}