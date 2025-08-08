# core/dispatcher.py

import logging
import yaml

from sensores.ultrasonicos import obstaculo_frontal
from core.motores       import inicializar_motor, enviar_comando_motor

def cargar_configuracion(path='config/settings.yaml'):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def leer_comando(path):
    try:
        with open(path, 'r') as f:
            return f.read().strip().lower()
    except FileNotFoundError:
        return None

def procesar_comando(comando, config, arduino=None):
    logging.info(f"Comando recibido: {comando}")

    if comando == 'avanza':
        pins = config['sensores']['ultrasonico']
        if obstaculo_frontal(
            config['umbral_obstaculo_cm'],
            pins['trigger_pin'],
            pins['echo_pin']
        ):
            logging.warning("Obstáculo detectado. Deteniendo.")
            enviar_comando_motor(arduino, 'M0', config)
        else:
            logging.info("Camino libre. Avanzando.")
            enviar_comando_motor(arduino, 'M1', config)

    elif comando == 'izquierda':
        enviar_comando_motor(arduino, 'M2', config)

    elif comando == 'derecha':
        enviar_comando_motor(arduino, 'M3', config)

    elif comando == 'atras':
        enviar_comando_motor(arduino, 'M4', config)

    elif comando == 'gira en tu mismo eje':
        enviar_comando_motor(arduino, 'M5', config)

    elif comando == 'detente':
        enviar_comando_motor(arduino, 'M0', config)

    else:
        logging.warning(f"Comando desconocido: {comando}")

def main():
    config = cargar_configuracion()
    logging.basicConfig(
        filename=config['log_path'],
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s'
    )

    arduino = inicializar_motor(config)

    comando = leer_comando(config['comando_path'])
    if comando:
        procesar_comando(comando, config, arduino)

if __name__ == '__main__':
    main()

