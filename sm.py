import requests
from datetime import datetime, timedelta

# CONFIGURACIÓN ==========================
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjE4MjNhNGE3LTMzZmItNDUwZi04NjFhLWI2NGI1ZTQzZmM2YSIsInRva2VuVmVyc2lvbiI6MSwiaWF0IjoxNzcyMDgzNTM1LCJleHAiOjE3NzIxMDUxMzV9.XoZOSEZV2iLtG7ZGU64BGCi3DWf14awX_ehc2vgToE4"
BASE_URL = "https://api.whaticket.com"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# MENSAJES ==========================
MENSAJE_INMEDIATO = "Hola {nombre} 👋 Te recordamos que tu pedido llegará el día {fecha}."
MENSAJE_PROGRAMADO1 = "Hola {nombre} 👋 Tu pedido llegará mañana."
MENSAJE_PROGRAMADO2 = "Hola {nombre} 👋 Tu pedido llegará hoy."

# CONFIGURACIÓN DE FECHAS
DIAS_A_SUMAR_TAG = 3
DIAS_A_SUMAR_PROGRAMADO1 = 2
HORA_ENVIO_PROGRAMADO1 = 20  # 8 PM
DIAS_A_SUMAR_PROGRAMADO2 = 3
HORA_ENVIO_PROGRAMADO2 = 8   # 8 AM

# DEPARTAMENTOS Y USUARIO
NOMBRE_QUEUE = "Confirmados Alicod" #Revisar
NOMBRE_QUEUE_DESTINO = "Registrado Alicod" #Revisar
USER_ID_DESTINO = "17018bb4-e8a7-4921-a98d-a854228560b1"  # 1Motorizado

# FUNCIONES ==========================
def obtener_tag_y_fecha():
    fecha_futura = datetime.now() + timedelta(days=DIAS_A_SUMAR_TAG)
    dia_tag = fecha_futura.strftime("%d")
    fecha_texto = fecha_futura.strftime("%d/%m")

    response = requests.get(f"{BASE_URL}/tag?pageNumber=1", headers=HEADERS)
    tags = response.json().get("tags", [])

    for tag in tags:
        if tag["name"] == dia_tag:
            print("Tag encontrado:", dia_tag)
            return tag["id"], fecha_texto

    return None, fecha_texto

def obtener_queue_id(nombre_queue):
    response = requests.get(f"{BASE_URL}/queue", headers=HEADERS)
    queues = response.json()
    for queue in queues:
        if queue["name"] == nombre_queue:
            print("Queue encontrada:", nombre_queue)
            return queue["id"]
    return None

def obtener_tickets(queue_id, tag_id):
    url = (
        f"{BASE_URL}/tickets?"
        f"pageNumber=1&"
        f"status=%22open%22&"
        f"queueIds=[\"{queue_id}\"]&"
        f"tagsIds=[\"{tag_id}\"]&"
        f"usersIds=[]"
    )
    response = requests.get(url, headers=HEADERS)
    return response.json().get("tickets", [])

def enviar_mensaje(ticket_id, texto):
    url = f"{BASE_URL}/messages/{ticket_id}"
    payload = {"body": texto}
    try:
        response = requests.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()
        print(f"Mensaje enviado → {response.status_code}")
    except requests.exceptions.HTTPError as e:
        print(f"Error enviando mensaje Ticket {ticket_id}: {e}")
        # Aquí podrías enviar plantilla si falla

def programar_mensaje(ticket_id, texto, dias_sumar, hora_envio):
    url = f"{BASE_URL}/messages/{ticket_id}"
    fecha_programada = datetime.now() + timedelta(days=dias_sumar)
    fecha_programada = fecha_programada.replace(
        hour=hora_envio, minute=0, second=0, microsecond=0
    )
    payload = {
        "body": texto,
        "fromMe": True,
        "isNote": False,
        "scheduleDate": fecha_programada.isoformat() + "Z",
        "signMessage": False
    }
    response = requests.post(url, json=payload, headers=HEADERS)
    print(f"Mensaje programado → {response.status_code}")

def transferir_ticket(ticket_id, queue_id, user_id):
    url = f"{BASE_URL}/tickets/{ticket_id}/transfer"
    payload = {"queueId": queue_id, "userId": user_id}
    try:
        response = requests.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()
        print(f"Ticket {ticket_id} transferido correctamente.")
    except requests.exceptions.HTTPError as e:
        print(f"Error transfiriendo ticket {ticket_id}: {e}")

# FLUJO PRINCIPAL ==========================
queue_id = obtener_queue_id(NOMBRE_QUEUE)
queue_id_destino = obtener_queue_id(NOMBRE_QUEUE_DESTINO)
tag_id, fecha_texto = obtener_tag_y_fecha()

if not tag_id:
    print("No existe el tag correspondiente al día:", fecha_texto)
    exit()
if not queue_id or not queue_id_destino:
    print("No se encontraron las queues necesarias")
    exit()

tickets = obtener_tickets(queue_id, tag_id)
print("\nTickets encontrados:", len(tickets))

for ticket in tickets:
    ticket_id = ticket["id"]
    nombre_contacto = ticket["contact"]["name"]

    mensaje_inmediato = MENSAJE_INMEDIATO.format(nombre=nombre_contacto, fecha=fecha_texto)
    mensaje_programado1 = MENSAJE_PROGRAMADO1.format(nombre=nombre_contacto)
    mensaje_programado2 = MENSAJE_PROGRAMADO2.format(nombre=nombre_contacto)

    enviar_mensaje(ticket_id, mensaje_inmediato)
    programar_mensaje(ticket_id, mensaje_programado1, DIAS_A_SUMAR_PROGRAMADO1, HORA_ENVIO_PROGRAMADO1)
    programar_mensaje(ticket_id, mensaje_programado2, DIAS_A_SUMAR_PROGRAMADO2, HORA_ENVIO_PROGRAMADO2)

    transferir_ticket(ticket_id, queue_id_destino, USER_ID_DESTINO)