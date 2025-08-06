const { ethers } = require("hardhat");

async function main() {
  const provider = new ethers.providers.JsonRpcProvider(process.env.POLYGON_RPC_URL);
  const wallet = new ethers.Wallet(`0x${process.env.PRIVATE_KEY}`, provider);

  console.log("👉 Dirección que se usará para desplegar:");
  console.log(wallet.address);

  const balance = await provider.getBalance(wallet.address);
  console.log("💰 MATIC disponibles:", ethers.utils.formatEther(balance));
}

main().catch((error) => {
  console.error("⛔ Error:", error);
  process.exit(1);
});
