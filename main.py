# main.py

import time
import os
import logging

from core.dispatcher import cargar_configuracion, leer_comando, procesar_comando
from core.motores     import inicializar_motor

def main():
    # 1. Cargo configuración y logging
    config = cargar_configuracion()
    logging.basicConfig(
        filename=config['log_path'],
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s'
    )

    # 2. Inicializo motor (simulado o real)
    arduino = inicializar_motor(config)

    # 3. Bucle continuo de lectura y procesamiento
    try:
        while True:
            comando = leer_comando(config['comando_path'])
            if comando:
                procesar_comando(comando, config, arduino)

                # 4. Borro o vacío el archivo de comando
                try:
                    os.remove(config['comando_path'])
                    logging.info("Archivo de comando borrado tras procesar.")
                except FileNotFoundError:
                    # Ya fue borrado o no existía
                    pass

            time.sleep(config.get('delay_loop', 0.5))

    except KeyboardInterrupt:
        logging.info("Interrupción por usuario. Terminando ejecución.")

if __name__ == '__main__':
    main()
