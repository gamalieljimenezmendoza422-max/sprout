# sensores/ultrasonicos.py

import logging
import time
import random

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    HAY_HARDWARE = True
    logging.info("Ultrasonico: modo hardware activado")
except ImportError:
    HAY_HARDWARE = False
    logging.info("Ultrasonico: modo simulación activado")

def leer_distancia_cm(trigger_pin, echo_pin):
    if HAY_HARDWARE:
        # Disparo de pulso ultrasónico
        GPIO.setup(trigger_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)
        GPIO.output(trigger_pin, GPIO.LOW)
        time.sleep(0.05)
        GPIO.output(trigger_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(trigger_pin, GPIO.LOW)

        # Espera señal de eco
        start = time.time()
        while GPIO.input(echo_pin) == 0:
            start = time.time()
        while GPIO.input(echo_pin) == 1:
            stop = time.time()

        duracion = stop - start
        distancia = duracion * 34300 / 2
        return distancia

    # Simulación: distancia aleatoria entre 5 y 100 cm
    distancia = random.uniform(5, 100)
    logging.info(f"[SIM] Distancia simulada: {distancia:.1f} cm")
    return distancia

def obstaculo_frontal(umbral_cm, trigger_pin, echo_pin):
    distancia = leer_distancia_cm(trigger_pin, echo_pin)
    logging.info(f"Distancia medida: {distancia:.1f} cm (umbral: {umbral_cm} cm)")

    return distancia <= umbral_cm
