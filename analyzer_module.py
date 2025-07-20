def analyze_contract(code: str) -> dict:
    findings = []

    # Revisión básica: funciones sin visibility explícita
    if "function" in code and "public" not in code and "private" not in code:
        findings.append("Algunas funciones no definen visibilidad")

    if "tx.origin" in code:
        findings.append("Uso de tx.origin detectado: riesgo de seguridad")

    if "revert" not in code and "require" not in code:
        findings.append("No hay validaciones explícitas en el contrato")

    return {
        "issues_found": findings,
        "total_issues": len(findings)
    }
