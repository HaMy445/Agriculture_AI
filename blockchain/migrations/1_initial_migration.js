const RiceDiseaseRecord = artifacts.require("RiceDiseaseRecord");

module.exports = function(deployer) {
  deployer.deploy(RiceDiseaseRecord).then(function() {
    console.log("✅ RiceDiseaseRecord deployed successfully!");
    console.log("Contract Address:", RiceDiseaseRecord.address);
  });
};
