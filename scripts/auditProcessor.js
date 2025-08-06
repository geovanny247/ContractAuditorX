const { JsonRpcProvider, formatUnits } = require("ethers");
const { Wallet, Contract } = require("ethers");
const fs = require("fs");
require("dotenv").config();

// 🌐 Configuración del proveedor RPC
const rpcUrl = process.env.POLYGON_RPC_URL?.trim();
if (!rpcUrl) throw new Error("❌ POLYGON_RPC_URL faltante");

const provider = new JsonRpcProvider(rpcUrl);

// 🔐 Validación de claves y contrato
const privateKey = process.env.PRIVATE_KEY?.trim();
const contractAddress = process.env.CONTRACT_ADDRESS?.trim();
const ABI = require("./AuditPaymentProcessor_ABI.json");

if (!privateKey || privateKey.length !== 64) throw new Error("❌ PRIVATE_KEY inválida");
if (!/^0x[a-fA-F0-9]{40}$/.test(contractAddress)) throw new Error("❌ CONTRACT_ADDRESS inválida");

// 🧠 Conexión con wallet y contrato
const wallet = new Wallet(privateKey, provider);
const contract = new Contract(contractAddress, ABI, wallet);

console.log(`🔗 Conectado al contrato: ${contract.address}`);
const logStream = fs.createWriteStream("./audit_log_usdc.txt", { flags: "a" });

async function monitorAndAudit() {
  const timestamp = new Date().toISOString();
  try {
    const usdcTokenAddress = await contract.usdcToken();
    const usdcContract = new Contract(
      usdcTokenAddress,
      ["function balanceOf(address) view returns (uint256)", "function decimals() view returns (uint8)"],
      provider
    );

    const decimals = await usdcContract.decimals();
    const rawBalance = await usdcContract.balanceOf(wallet.address);
    const balance = parseFloat(formatUnits(rawBalance, decimals));

    logStream.write(`[${timestamp}] 💳 Balance USDC: ${balance}\n`);
    console.log(`💳 Balance USDC: ${balance}`);

    const rawFee = await contract.auditFee();
    const fee = parseFloat(formatUnits(rawFee, decimals));

    if (balance >= fee) {
      logStream.write(`[${timestamp}] 🟢 Ejecutando auditoría...\n`);
      console.log(`🚀 Ejecutando auditoría...`);

      const tx = await contract.payForAudit("AuditorX");
      logStream.write(`[${timestamp}] ⏳ TX enviada: ${tx.hash}\n`);

      const receipt = await tx.wait();
      logStream.write(`[${timestamp}] ✅ TX confirmada: ${receipt.transactionHash}\n`);
    } else {
      logStream.write(`[${timestamp}] 🛑 Fondos insuficientes (requiere ${fee} USDC)\n`);
      console.log(`🛑 Fondos insuficientes (requiere ${fee} USDC)`);
    }
  } catch (err) {
    logStream.write(`[${timestamp}] ❌ ERROR: ${err.message || err}\n`);
    console.error(`🚨 ERROR: ${err.message || err}`);
  }
}

logStream.write(`\n===== 🎯 Monitor USDC AuditorX iniciado @ ${new Date().toISOString()} =====\n`);
console.log("🟢 Monitor activo. Revisando cada 30 segundos...");
setInterval(monitorAndAudit, 30_000);
