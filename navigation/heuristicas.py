import math
from typing import Tuple

def euclidea(n: Tuple[float, float], m: Tuple[float, float]) -> float:
    """
    Calcula la distancia euclídea entre dos puntos n y m.
    Parámetros:
      n, m: tuplas (x, y)
    Retorna:
      hipotenusa sqrt((dx)^2 + (dy)^2)
    """
    dx, dy = n[0] - m[0], n[1] - m[1]
    return math.hypot(dx, dy)

def manhattan(n: Tuple[float, float], m: Tuple[float, float]) -> float:
    """
    Calcula la distancia Manhattan (enrejado) entre n y m.
    Parámetros:
      n, m: tuplas (x, y)
    Retorna:
      |dx| + |dy|
    """
    return abs(n[0] - m[0]) + abs(n[1] - m[1])
