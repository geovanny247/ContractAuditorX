require("dotenv").config();
require("@nomicfoundation/hardhat-toolbox");

// 🔐 Plugin de auditoría personalizado
require("./hardhat-contractauditorx/index.cjs");

const { auditBeforeDeploy } = require("./auditBeforeDeploy");

(async () => {
  try {
    await auditBeforeDeploy();
    console.log("✅ Auditoría completada. Continuando con el deploy...");
  } catch (err) {
    console.error("❌ Error en la auditoría:", err.message || err);
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

