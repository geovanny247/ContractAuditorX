require("dotenv").config();
const { ethers } = require("ethers");

async function main() {
  const provider = new ethers.JsonRpcProvider(process.env.POLYGON_RPC_URL);
  const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);
  const balance = await provider.getBalance(wallet.address);
  console.log("💰 Balance real:", ethers.formatEther(balance), "MATIC");
}

main().catch(console.error);

