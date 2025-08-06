import fetch from "node-fetch";

const generateDummyContract = (i) => `
pragma solidity ^0.8.0;
contract Dummy${i} {
    uint256 public value;
    function set(uint256 _v) public { value = _v; }
}
`;

const loopAudit = async () => {
  for (let i = 0; i < 1000; i++) {
    const code = generateDummyContract(i);

    try {
      const res = await fetch("https://contractauditorx.onrender.com/audit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });

      const json = await res.json();

      if (json.payment_url) {
        console.log(`✅ Dummy${i} auditado. Enlace de pago generado: ${json.payment_url}`);
      } else {
        console.warn(`⚠️ Dummy${i} falló en la auditoría. Respuesta: ${JSON.stringify(json)}`);
      }
    } catch (err) {
      console.error(`❌ Error al auditar Dummy${i}:`, err.message);
    }
  }
};

loopAudit();
