"""Lógica pura de evaluación de resultados contra límites de especificación."""


def evaluar(valor: float, minimo: float | None, maximo: float | None) -> bool:
    """True si el valor cumple la especificación (límites inclusivos, ambos opcionales)."""
    if minimo is not None and valor < minimo:
        return False
    if maximo is not None and valor > maximo:
        return False
    return True


def validar_limites(minimo: float | None, maximo: float | None) -> None:
    if minimo is not None and maximo is not None and minimo > maximo:
        raise ValueError("El límite mínimo no puede ser mayor que el máximo")
