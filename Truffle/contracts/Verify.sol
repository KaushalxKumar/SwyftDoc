pragma solidity 0.8.0;

import "./Certify.sol";

contract Verify {
    Certify public certifyContract;

    constructor(address _certifyContractAddress) {
        certifyContract = Certify(_certifyContractAddress);
    }

    // Function to verify a document given its hash
    function verifyDocument(bytes32 _hash) public view returns (address, bytes memory, bytes memory) {
        (address owner, bytes memory signature, bytes memory publicKey, bytes32 hash) = certifyContract.documents(_hash);

        require(owner != address(0), "Document with this hash does not exist");

        return (owner, signature, publicKey);
    }
}