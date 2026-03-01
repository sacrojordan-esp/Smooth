import requests

# CONFIGURACIÓN ==========================
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImNmMTc1ZTY4LTljMjQtNGFmMi1hNjFmLTRkNDczMjljM2ZiNCIsInRva2VuVmVyc2lvbiI6ODIsImlhdCI6MTc3MjIyNDY0OCwiZXhwIjoxNzcyMjQ2MjQ4fQ.ycFnpGz2q4I2OHWSn-FwAcEHDIdhIzEghr2_IGthKGE"
BASE_URL = "https://api.whaticket.com"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# CONSULTAS ==========================
QUEUE_CONFIRMADO = "CONFIRMADO ALICOD"
QUEUE_REGISTRADO = "REGISTRADO ALICOD"
USUARIO_MOTORIZADO = "1MOTORIZADOS"

# FUNCIONES ==========================
def obtener_queue_id_por_nombre(nombre_queue):
    response = requests.get(f"{BASE_URL}/queue", headers=HEADERS)
    queues = response.json()

    for queue in queues:
        if queue["name"] == nombre_queue:
            return queue["id"]
    return None

def obtener_user_id_por_nombre(nombre_usuario):
    response = requests.get(f"{BASE_URL}/users", headers=HEADERS)
    data = response.json()
    users = data.get("users", [])

    for user in users:
        if user["name"] == nombre_usuario:
            return user["id"]
    return None

def obtener_connection_id_por_nombre(nombre_connection):
    response = requests.get(f"{BASE_URL}/connections", headers=HEADERS)
    connections = response.json()

    for conn in connections:
        if conn["name"] == nombre_connection:
            return conn["id"]
    return None

# EJECUCIÓN ==========================
if __name__ == "__main__":
    print("=== CONSULTAS ===\n")

    user_id = obtener_user_id_por_nombre(USUARIO_MOTORIZADO)
    print(f"User ID ({USUARIO_MOTORIZADO}): {user_id}\n")

    queue_id_confirmado = obtener_queue_id_por_nombre(QUEUE_CONFIRMADO)
    print(f"Queue ID ({QUEUE_CONFIRMADO}): {queue_id_confirmado}\n")

    queue_id_registrado = obtener_queue_id_por_nombre(QUEUE_REGISTRADO)
    print(f"Queue ID ({QUEUE_REGISTRADO}): {queue_id_registrado}\n")
