const { auditBeforeDeploy, generateReport } = require("contractauditorx-sdk");

module.exports = async (bytecode) => {
  const result = await auditBeforeDeploy(bytecode);
  const report = await generateReport(bytecode);
  return {
    passed: result.passed,
    report
  };
};
