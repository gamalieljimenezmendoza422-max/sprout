import heapq
import logging
from typing import Any, Dict, List, Tuple, Callable, Optional

logger = logging.getLogger("navigation.planificar")
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '{"time":"%(asctime)s","node":"%(node)s","g":%(g_value)s,"h":%(h_value)s,"f":%(f_value)s,"event":"%(message)s"}'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

Vecino = Tuple[Any, float]  # (nodo_vecino, coste)

def planificar_ruta(
    inicio: Any,
    objetivo: Any,
    vecinos: Callable[[Any], List[Vecino]],
    heuristica: Callable[[Any, Any], float]
) -> Optional[List[Any]]:
    open_set: List[Tuple[float, Any]] = []
    heapq.heappush(open_set, (heuristica(inicio, objetivo), inicio))

    g_score: Dict[Any, float] = {inicio: 0.0}
    parent: Dict[Any, Any] = {}
    closed_set: set = set()

    while open_set:
        f_current, nodo = heapq.heappop(open_set)

        if nodo == objetivo:
            ruta = [nodo]
            while nodo in parent:
                nodo = parent[nodo]
                ruta.append(nodo)
            return list(reversed(ruta))

        closed_set.add(nodo)

        for vecino, coste in vecinos(nodo):
            tentative_g = g_score[nodo] + coste

            if vecino in closed_set and tentative_g >= g_score.get(vecino, float("inf")):
                continue

            if tentative_g < g_score.get(vecino, float("inf")):
                parent[vecino] = nodo
                g_score[vecino] = tentative_g
                f_score = tentative_g + heuristica(vecino, objetivo)

                extra = {
                    "node": repr(vecino),
                    "g_value": tentative_g,
                    "h_value": heuristica(vecino, objetivo),
                    "f_value": f_score
                }
                logger.debug(f"Pushing to open_set: {vecino}", extra=extra)

                heapq.heappush(open_set, (f_score, vecino))

    return None
