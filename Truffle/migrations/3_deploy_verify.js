const Verify = artifacts.require("Verify");
const Certify = artifacts.require("Certify"); // Import the Certify contract

module.exports = async function (deployer) {
  // Deploy Certify contract first
  await deployer.deploy(Certify);
  const certifyInstance = await Certify.deployed();

  // Deploy Verify contract and pass the Certify contract's address
  await deployer.deploy(Verify, certifyInstance.address);
};
