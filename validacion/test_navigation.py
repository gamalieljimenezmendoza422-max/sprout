import pytest
import sensores.ultrasonicos as us
from core import navigation

# Desactivar warnings de GPIO
us.GPIO.setwarnings(False)

class FakeArduino:
    def __init__(self):
        self.commands = []

def test_planificar_ruta_simple():
    destino = (5, 10)
    ruta = navigation.planificar_ruta(destino)
    assert isinstance(ruta, list)
    assert ruta == [destino]

@pytest.fixture
def config_minimo():
    return {
        'sensores': {
            'ultrasonico': {
                'trigger_pin': 17,
                'echo_pin': 27,
            }
        },
        'umbral_obstaculo_cm': 10
    }

def test_navegar_waypoints_sin_obstaculo(monkeypatch, config_minimo):
    fake_arduino = FakeArduino()
    # Primero no hay obstáculo, luego sí para salir del bucle
    estados = [False, True]
    monkeypatch.setattr(
        navigation,
        'obstaculo_frontal',
        lambda umbral, trig, echo: estados.pop(0)
    )
    monkeypatch.setattr(
        'core.motores.enviar_comando_motor',
        lambda arduino, cmd, cfg: arduino.commands.append(cmd)
    )

    navigation.navegar_waypoints([(1, 1)], config_minimo, fake_arduino)

    # Debe enviar primero M1 y luego M0
    assert fake_arduino.commands == ['M1', 'M0']

def test_navegar_waypoints_con_obstaculo_inmediato(monkeypatch, config_minimo):
    fake_arduino = FakeArduino()
    # Obstáculo inmediato
    monkeypatch.setattr(
        navigation,
        'obstaculo_frontal',
        lambda umbral, trig, echo: True
    )
    monkeypatch.setattr(
        'core.motores.enviar_comando_motor',
        lambda arduino, cmd, cfg: arduino.commands.append(cmd)
    )

    navigation.navegar_waypoints([(2, 3)], config_minimo, fake_arduino)

    # Solo debe mandar M0
    assert fake_arduino.commands == ['M0']

