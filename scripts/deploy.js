const fs = require("fs");
const {
  JsonRpcProvider,
  Wallet,
  Contract,
  parseEther,
  formatEther
} = require("ethers");
require("dotenv").config();

// 🌐 Configuración del proveedor RPC
const rpcUrl = process.env.POLYGON_RPC_URL?.trim();
if (!rpcUrl) {
  console.error("❌ POLYGON_RPC_URL faltante en .env");
  process.exit(1);
}
const provider = new JsonRpcProvider(rpcUrl);

// 🔐 Validación de claves y contrato
const privateKey = process.env.PRIVATE_KEY?.trim();
const contractAddress = process.env.CONTRACT_ADDRESS?.trim();
const ABI = require("./AuditorX_ABI.json");

if (!privateKey || privateKey.length !== 64) {
  console.error("❌ PRIVATE_KEY faltante o inválido");
  process.exit(1);
}

if (!contractAddress || !/^0x[a-fA-F0-9]{40}$/.test(contractAddress)) {
  console.error(`❌ CONTRACT_ADDRESS inválida: '${contractAddress}'`);
  process.exit(1);
}

// 🧠 Conexión con contrato y wallet
const wallet = new Wallet(privateKey, provider);
const contract = new Contract(contractAddress, ABI, wallet);

// 🎯 Confirmar conexión y mostrar address del contrato
console.log(`🔗 Conectado al contrato: ${contract.address}`);

// 💰 Umbral mínimo para ejecutar auditoría
const thresholdMATIC = parseFloat(formatEther(parseEther("0.01")));

// 📄 Setup de logs
const logStream = fs.createWriteStream("./audit_log_mainnet.txt", { flags: "a" });

// 📈 Balance previo
let lastBalance = null;

async function monitorAndTriggerAudit() {
  const timestamp = new Date().toISOString();
  try {
    const currentBN = await provider.getBalance(wallet.address);
    const currentBalance = parseFloat(formatEther(currentBN));
    logStream.write(`[${timestamp}] 📡 Balance actual: ${currentBalance.toFixed(6)} MATIC\n`);

    if (currentBalance >= thresholdMATIC) {
      logStream.write(`[${timestamp}] 🚀 Ejecutando auditoría...\n`);
      console.log(`🚀 Ejecutando auditoría...`);

      const preTxBalance = currentBalance;

      const tx = await contract.payForAudit("AuditorX");
      logStream.write(`[${timestamp}] ⏳ TX enviada: ${tx.hash}\n`);

      const receipt = await tx.wait();
      logStream.write(`[${timestamp}] ✅ TX confirmada: ${receipt.transactionHash}\n`);

      const postTxBN = await provider.getBalance(wallet.address);
      const postTxBalance = parseFloat(formatEther(postTxBN));
      const delta = postTxBalance - preTxBalance;

      if (delta > 0) {
        logStream.write(`[${timestamp}] 📈 Ganancia neta: +${delta.toFixed(6)} MATIC\n`);
        console.log(`📈 Ganancia neta: +${delta.toFixed(6)} MATIC`);
      } else if (delta < 0) {
        logStream.write(`[${timestamp}] 📉 Pérdida neta: ${delta.toFixed(6)} MATIC\n`);
        console.log(`📉 Pérdida neta: ${delta.toFixed(6)} MATIC`);
      } else {
        logStream.write(`[${timestamp}] 🟨 Sin variación de saldo\n`);
        console.log(`🟨 Sin variación de saldo`);
      }

      lastBalance = postTxBalance;
    } else {
      logStream.write(`[${timestamp}] 💤 Fondos insuficientes\n`);
      console.log(`🛑 Balance insuficiente: ${currentBalance.toFixed(6)} MATIC`);
    }
  } catch (err) {
    logStream.write(`[${timestamp}] ❌ ERROR: ${err.message || err}\n`);
    console.error(`🚨 ERROR: ${err.message || err}`);
  }
}

logStream.write(`\n===== 🚦 Monitor AuditorX iniciado @ ${new Date().toISOString()} =====\n`);
console.log("🟢 Monitor activo. Revisando cada 30 segundos...");
setInterval(monitorAndTriggerAudit, 30_000);













