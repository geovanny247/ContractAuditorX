const { generateReport } = require("./generateReport");
const { checkPaymentStatus } = require("./checkPaymentStatus");
const config = require("./auditor.config");

async function auditBeforeDeploy() {
  const report = await generateReport();
  console.log("🛡️ Informe de auditoría:", report);

  if (report.total_issues > 0) {
    console.log("⚠️ Se encontraron problemas. Requiere pago.");
    const paid = await checkPaymentStatus(config.paymentUrl);
    if (!paid && config.blockDeployIfUnpaid) {
      throw new Error("🚫 El contrato no puede desplegarse sin pagar la auditoría.");
    }
  } else {
    console.log("✅ Auditoría limpia. Puedes continuar.");
  }
}

module.exports = { auditBeforeDeploy };
