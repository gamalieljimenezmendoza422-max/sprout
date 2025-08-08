import pytest
from navigation.planificar import planificar_ruta
from navigation.heuristicas import euclidea

# Grafo lineal para ruta simple
def vecinos_lineal(nodo):
    mapa = {
        "A": [("B", 1)],
        "B": [("A", 1), ("C", 1)],
        "C": [("B", 1)]
    }
    return mapa.get(nodo, [])

def test_ruta_simple():
    ruta = planificar_ruta("A", "C", vecinos_lineal, lambda x, y: 0)
    assert ruta == ["A", "B", "C"]

def test_no_existe_ruta():
    ruta = planificar_ruta("X", "Y", lambda x: [], lambda x, y: 0)
    assert ruta is None

def test_euclidea_heuristica():
    puntos = [(0, 0), (1, 1), (2, 2)]
    vecinos = lambda n: [((n[0]+1, n[1]+1), 1)] if n != puntos[-1] else []
    ruta = planificar_ruta(puntos[0], puntos[-1], vecinos, euclidea)
    assert ruta == puntos
