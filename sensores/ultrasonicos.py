import RPi.GPIO as GPIO

# Desactivar advertencias de canales en uso
GPIO.setwarnings(False)

# Resto de imports y funciones
GPIO.setmode(GPIO.BCM)

def obstaculo_frontal(umbral_cm, trigger_pin, echo_pin):
    GPIO.setup(trigger_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)
    # lógica de ultrasonidos...
    # return True/False

