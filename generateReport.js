async function generateReport() {
  // Aquí puedes conectar con tu bot en Render o usar lógica local
  return {
    issues_found: ["No hay validaciones explícitas en el contrato"],
    total_issues: 1
  };
}

module.exports = { generateReport };
