require("dotenv").config();
require("@nomicfoundation/hardhat-toolbox");

const { auditBeforeDeploy } = require("./auditBeforeDeploy");

(async () => {
  try {
    await auditBeforeDeploy();
    console.log("✅ Auditoría completada. Continuando con el deploy...");
  } catch (err) {
    console.error(err.message);
    process.exit(1);
  }
})();

module.exports = {
  solidity: "0.8.28",
  defaultNetwork: "polygon",
  networks: {
    polygon: {
      url: process.env.POLYGON_RPC_URL,
      accounts: [`0x${process.env.PRIVATE_KEY}`],
    },
  },
};

