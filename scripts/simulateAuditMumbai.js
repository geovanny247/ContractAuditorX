require("dotenv").config();
const { ethers } = require("hardhat");
const fs = require("fs");

// ✅ Validar variables de entorno antes de ejecutar
const requiredEnv = ["CONTRACT_ADDRESS", "PRIVATE_KEY", "RPC_URL", "CHAIN_ID"];
requiredEnv.forEach((key) => {
  if (!process.env[key]) {
    throw new Error(`❌ Falta la variable ${key} en .env`);
  }
});

async function main() {
  const contractAddress = process.env.CONTRACT_ADDRESS;

  // 📦 Asegura que la compilación está lista
  if (!fs.existsSync(`artifacts/contracts/AuditorX.sol/AuditorX.json`)) {
    throw new Error(`❌ AuditorX.json no encontrado. Ejecuta: npx hardhat compile`);
  }

  const auditBot = await ethers.getContractAt("AuditorX", contractAddress);

  console.log("🔐 Ejecutando pago simulado...");
  const tx = await auditBot.payForAudit({
    value: ethers.utils.parseEther("0.1"),
  });

  console.log(`🔁 TX enviada: ${tx.hash}`);
  const receipt = await tx.wait();

  const success = receipt.status === 1;
  console.log(success ? "✅ TX confirmada, audit solicitado con éxito." : "❌ TX fallida. Revisa el contrato o gas.");

  const logData = [
    `📅 ${new Date().toISOString()}`,
    `TX: ${tx.hash}`,
    `Contract: ${contractAddress}`,
    `Block: ${receipt.blockNumber}`,
    `Gas Used: ${receipt.gasUsed.toString()}`
  ].join("\n") + "\n\n";

  fs.appendFileSync("audit_log.txt", logData);
  console.log("📄 Log guardado en audit_log.txt");
}

main().catch((error) => {
  console.error("💥 Error en la simulación:", error);
  process.exit(1);
});
