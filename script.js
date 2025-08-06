const auditContract = async (address) => {
  const reportDiv = document.getElementById("report");
  reportDiv.innerText = "⏳ Auditando contrato...";

  try {
    const response = await fetch("https://contractauditorx.onrender.com/audit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ code: address })  // 🔥 Esto es clave: 'code', no 'address'
    });

    const result = await response.json();

    if (result.status === "success") {
      reportDiv.innerHTML = `
        ✅ ${result.audit_report}<br>
        💳 <a href="${result.payment_url}" target="_blank">Pagar con Coinbase</a>
      `;
    } else {
      reportDiv.innerText = `❌ Error: ${result.error || "Respuesta inválida del servidor."}`;
    }

  } catch (error) {
    reportDiv.innerText = `🔥 Error de red o CORS: ${error.message}`;
    console.error("Error durante la auditoría:", error);
  }
};
