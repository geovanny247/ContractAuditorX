async function checkPaymentStatus(paymentUrl) {
  console.log(`💳 Verificando pago en: ${paymentUrl}`);
  // Simulación: en producción deberías consultar Coinbase Commerce API
  return false; // Cambia a true si detectas que se ha pagado
}

module.exports = { checkPaymentStatus };
