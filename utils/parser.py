import re

def normalize_code(code: str) -> str:
    """
    Limpia el contrato eliminando comentarios, espacios redundantes
    y caracteres invisibles que puedan generar falsos positivos.
    """
    # Eliminar comentarios multilinea
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
    # Eliminar comentarios simples
    code = re.sub(r"//.*", "", code)
    # Eliminar espacios y saltos innecesarios
    code = re.sub(r"\s+", " ", code).strip()
    return code

def extract_functions(code: str) -> list:
    """
    Extrae nombres de funciones definidas en el contrato.
    """
    pattern = r"function\s+(\w+)\s*\("
    matches = re.findall(pattern, code)
    return matches

def has_fallback(code: str) -> bool:
    """
    Detecta si el contrato tiene una función fallback o receive.
    """
    return "fallback()" in code or "receive()" in code
