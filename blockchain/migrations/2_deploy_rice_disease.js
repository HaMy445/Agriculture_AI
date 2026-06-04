const RiceDiseaseRecord = artifacts.require("RiceDiseaseRecord");

module.exports = function(deployer) {
  deployer.deploy(RiceDiseaseRecord);
};
