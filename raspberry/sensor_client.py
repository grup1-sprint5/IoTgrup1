"""
Script autònom per a la Raspberry Pi – LightCar IoT
====================================================
Llegeix el sensor ultrasònic HC-SR04 i envia les dades
al microservei FastAPI cada 2 segons via HTTP POST.

Dependències (instal·lar UNA SOLA VEGADA a la Raspberry):
    pip install gpiozero requests

Ús:
    python3 sensor_client.py

Notes:
  - No necessita cap fitxer del projecte FastAPI.
  - Canvia API_URL per la IP real del servidor que corre el microservei.
"""

from gpiozero import DistanceSensor
import time
import requests

# IP i port del servidor on corre el microservei FastAPI
# Per trobar la IP del servidor: ip addr   o bé   hostname -I
API_URL = "http://192.168.226.125:8001/api/sensor-data"

# Pins GPIO (numeració BCM)
GPIO_ECHO    = 24
GPIO_TRIGGER = 23

DEVICE_ID   = "lightcar_01"
SENSOR_TYPE = "ultrasonic"
INTERVAL_S  = 2   # Segons entre lectures

# ─────────────────────────────────────────────────────────────────────────────

sensor = DistanceSensor(echo=GPIO_ECHO, trigger=GPIO_TRIGGER, max_distance=2)

print(f"--- LightCar en línia: Enviant dades a {API_URL} ---")

try:
    while True:
        distancia_cm = round(sensor.distance * 100, 2)

        payload = {
            "device_id":   DEVICE_ID,
            "sensor_type": SENSOR_TYPE,
            "value":       distancia_cm,
            "unit":        "cm",
            "timestamp":   time.strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            response = requests.post(API_URL, json=payload, timeout=2)

            if response.status_code in (200, 201):
                print(f"Enviat: {distancia_cm} cm  →  API: {response.status_code}")
            else:
                print(f"Error API: {response.status_code} – {response.text}")

        except requests.exceptions.ConnectionError:
            print("Connexió refusada: comprova la IP del servidor i que el microservei estigui arrencat")
        except requests.exceptions.Timeout:
            print("Timeout: l'API no ha respost en 2 s")
        except requests.exceptions.RequestException as e:
            print(f"Error inesperat: {e}")

        time.sleep(INTERVAL_S)

except KeyboardInterrupt:
    print("\nConnexió tancada. Fins aviat!")
