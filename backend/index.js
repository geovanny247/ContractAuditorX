const express = require("express");
const app = express();
const port = 8000;

app.use(express.json());

const { validatePayment } = require("./utils/validatePayment");
const { runAudit } = require("./auditEngine");

app.post("/api/audit", async (req, res) => {
  const { user, contractAddress } = req.body;

  const paid = await validatePayment(user, contractAddress);
  if (!paid) return res.status(403).json({ error: "Payment not found" });

  const report = await runAudit(contractAddress);
  return res.json({ auditReport: report });
});

app.listen(port, () => {
  console.log(`🔎 Audit bot running at http://localhost:${port}`);
});
