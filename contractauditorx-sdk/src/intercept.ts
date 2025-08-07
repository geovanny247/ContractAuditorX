import { createThirdwebClient } from "thirdweb";
import fetch from "node-fetch";

export const client = createThirdwebClient({
  clientId: "3c1baec646d89b0b284bbcb5a73e56b3",
  secretKey: "TU_SECRET_KEY_COMPLETO"
});

export async function auditBeforeDeploy(contractCode: string) {
  const auditResponse = await fetch("https://contractauditorx.onrender.com/audit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: contractCode })
  });

  const result = await auditResponse.json();

  if (!result.paid) {
    console.log("🚫 Auditoría pendiente. Paga aquí:", result.payment_link);
    throw new Error("Debes pagar la auditoría antes de desplegar.");
  }

  console.log("✅ Auditoría pagada. Puedes continuar con el deploy.");
}
