import fetch from "node-fetch";

export async function isPaymentConfirmed(paymentId: string): Promise<boolean> {
  const response = await fetch(`https://api.commerce.coinbase.com/checkouts/${paymentId}`, {
    headers: {
      "X-CC-Api-Key": "TU_API_KEY",
      "X-CC-Version": "2022-03-22"
    }
  });

  const data = await response.json();
  return data.data.payments && data.data.payments.length > 0;
}
