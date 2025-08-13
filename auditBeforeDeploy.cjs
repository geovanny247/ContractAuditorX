import { generateReport } from "./generateReport.js";
import { checkPaymentStatus } from "./checkPaymentStatus.js";
import config from "./auditor.config.js";

export async function auditBeforeDeploy() {
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

