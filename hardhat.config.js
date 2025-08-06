require("dotenv").config();
require("@nomicfoundation/hardhat-toolbox");

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

