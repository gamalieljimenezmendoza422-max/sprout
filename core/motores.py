# core/motores.py

import logging

try:
    import serial
    ENTORNO_REAL = True
except ImportError:
    ENTORNO_REAL = False

class MotorSimulado:
    def write(self, data):
        logging.info(f"[SIMULADO] Comando al motor: {data.decode()}")

def inicializar_motor(config):
    if config['modo_simulacion']:
        logging.info("Modo simulación activado. Usando motor simulado.")
        return MotorSimulado()
    else:
        try:
            arduino = serial.Serial(
                config['puerto_serial'],
                config['baudrate'],
                timeout=1
            )
            logging.info(f"Arduino conectado en {config['puerto_serial']}")
            return arduino
        except Exception as e:
            logging.error(f"No se pudo conectar al Arduino: {e}")
            return MotorSimulado()

def enviar_comando_motor(arduino, comando, config):
    try:
        arduino.write(comando.encode())
        logging.info(f"Comando enviado al motor: {comando}")
    except Exception as e:
        logging.error(f"Error al enviar comando: {e}")
