const axios = require('axios');

async function checkPaymentStatus(chargeId) {
  const apiKey = process.env.COINBASE_API_KEY; // Asegúrate de tener esto en tu .env
  const url = `https://api.commerce.coinbase.com/charges/${chargeId}`;

  try {
    const response = await axios.get(url, {
      headers: {
        'X-CC-Api-Key': apiKey,
        'X-CC-Version': '2018-03-22'
      }
    });

    const status = response.data.data.timeline.slice(-1)[0].status;
    console.log(`🔍 Estado del pago: ${status}`);

    return status === 'COMPLETED';
  } catch (error) {
    console.error('❌ Error al verificar el pago:', error.message);
    return false;
  }
}

module.exports = { checkPaymentStatus };
