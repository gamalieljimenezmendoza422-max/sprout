# core/navigation.py

import logging
from sensores.ultrasonicos import obstaculo_frontal

def planificar_ruta(destino, mapa=None):
    """
    Crea una lista de waypoints hasta 'destino'.
    - destino: tupla (x, y) en coordenadas locales
    - mapa: estructura opcional con obstáculos
    Devuelve: lista de waypoints [(x1,y1), (x2,y2), ...]
    """
    # TODO: reemplaza esto con A*, Dijkstra o tu heurística
    return [destino]

def navegar_waypoints(waypoints, config, arduino):
    """
    Recorre secuencialmente cada waypoint:
    - Llama a 'avanza' hasta llegar o detectar un obstáculo.
    - Si hay obstáculo frontal, detiene el avance.
    """
    trigger = config['sensores']['ultrasonico']['trigger_pin']
    echo    = config['sensores']['ultrasonico']['echo_pin']
    umbral  = config['umbral_obstaculo_cm']

    for wp in waypoints:
        logging.info(f"Navegando a waypoint {wp}")
        # Avanza mientras no haya obstáculo
        while not obstaculo_frontal(umbral, trigger, echo):
            from core.motores import enviar_comando_motor
            enviar_comando_motor(arduino, 'M1', config)
        logging.warning("Obstáculo detectado, deteniendo navegación")
        from core.motores import enviar_comando_motor
        enviar_comando_motor(arduino, 'M0', config)
        break  # aquí podrías replanificar o abortar

def main_navigation(destino, config, arduino):
    """
    Punto de entrada de navegación:
    1) Planifica ruta
    2) Ejecuta waypoints
    """
    ruta = planificar_ruta(destino)
    navegar_waypoints(ruta, config, arduino)
