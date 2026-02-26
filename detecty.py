import requests
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjE4MjNhNGE3LTMzZmItNDUwZi04NjFhLWI2NGI1ZTQzZmM2YSIsInRva2VuVmVyc2lvbiI6MSwiaWF0IjoxNzcyMDgzNTM1LCJleHAiOjE3NzIxMDUxMzV9.XoZOSEZV2iLtG7ZGU64BGCi3DWf14awX_ehc2vgToE4"
BASE_URL = "https://api.whaticket.com"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def obtener_queue_id_por_nombre(nombre_queue):
    response = requests.get(f"{BASE_URL}/queue", headers=HEADERS)
    queues = response.json()

    for queue in queues:
        if queue["name"] == nombre_queue:
            return queue["id"]
    return None

def obtener_user_id_por_nombre(nombre_usuario):
    response = requests.get(f"{BASE_URL}/users", headers=HEADERS)
    data = response.json()  # Esto probablemente es un diccionario
    users = data.get("users", [])  # Accedemos a la lista de usuarios

    for user in users:
        if user["name"] == nombre_usuario:
            return user["id"]
    return None

user = "1MOTORIZADO"
queueC = "Confirmados Alicod"
queueR = "Registrado Alicod"

user_id = obtener_user_id_por_nombre(user)
print(f"User ID {user}:", user_id)

queue_id_registrado = obtener_queue_id_por_nombre(queueC)
print(F"Queue ID {queueC}:", queue_id_registrado)
queue_id_registrado = obtener_queue_id_por_nombre("Confirmados Alicod")
print(F"Queue ID {queueR}", queue_id_registrado)