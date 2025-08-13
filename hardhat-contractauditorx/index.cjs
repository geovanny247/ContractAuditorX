import { auditBeforeDeploy } from "contractauditorx-sdk";

task("audit", "Audita el contrato antes de desplegar")
  .addParam("contract", "Ruta al contrato")
  .setAction(async ({ contract }, hre) => {
    const result = await auditBeforeDeploy(contract);
    console.log("Resultado de auditoría:", result);
  });
