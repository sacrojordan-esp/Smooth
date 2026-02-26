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
MENSAJE_PROGRAMADO2 = "Hola {nombre} 👋 Tu pedido llegará Hoy."

DIAS_A_SUMAR_TAG = 3

DIAS_A_SUMAR_PROGRAMADO1 = 2
HORA_ENVIO_PROGRAMADO1 = 20  # 8 PM

DIAS_A_SUMAR_PROGRAMADO2 = 3
HORA_ENVIO_PROGRAMADO2 = 8  # 8 AM

NOMBRE_QUEUE = "Confirmados Alicod"

# FUNCIONES AUXILIARES ==========================

def obtener_tag_y_fecha(): #Tag de dia de llegada 01 y fecha 01/03
    fecha_futura = datetime.now() + timedelta(days=DIAS_A_SUMAR_TAG)

    dia_tag = fecha_futura.strftime("%d")       # Para el TAG (01)
    fecha_texto = fecha_futura.strftime("%d/%m")  # Para el mensaje (01/03)

    response = requests.get(f"{BASE_URL}/tag?pageNumber=1", headers=HEADERS)
    tags = response.json().get("tags", [])

    for tag in tags:
        if tag["name"] == dia_tag:
            print("Tag encontrado:", dia_tag)
            return tag["id"], fecha_texto

    return None, fecha_texto


def obtener_queue_id(): #ID del departamento
    response = requests.get(f"{BASE_URL}/queue", headers=HEADERS)
    queues = response.json()

    for queue in queues:
        if queue["name"] == NOMBRE_QUEUE:
            print("Queue encontrada:", NOMBRE_QUEUE)
            return queue["id"]

    return None


def obtener_tickets(queue_id, tag_id): #Tickets activos que cumplen con TAG Y DEPARTAMENTO
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

# FUNCIONES PRINCIPALES ==========================

def enviar_mensaje(ticket_id, texto): #NOT0
    url = f"{BASE_URL}/messages/{ticket_id}"
    payload = {"body": texto}

    try:
        response = requests.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()  # Esto lanza excepción si status >= 400
        print(f"Mensaje enviado → {response.status_code}")
    except requests.exceptions.HTTPError as e:
        print(f"Error enviando mensaje: Ticket {ticket_id}: {e}")
        #enviar_plantilla(ticket_id)


def programar_mensaje1(ticket_id, texto): #NOT1
    url = f"{BASE_URL}/messages/{ticket_id}"

    fecha_programada = datetime.now() + timedelta(days=DIAS_A_SUMAR_PROGRAMADO1)
    fecha_programada = fecha_programada.replace(
        hour=HORA_ENVIO_PROGRAMADO1,
        minute=0,
        second=0,
        microsecond=0
    )

    payload = {
        "body": texto,
        "fromMe": True,
        "isNote": False,
        "scheduleDate": fecha_programada.isoformat() + "Z",
        "signMessage": False
    }

    response = requests.post(url, json=payload, headers=HEADERS)
    print(f"Mensaje 1 programado → {response.status_code}")

def programar_mensaje2(ticket_id, texto): #NOT2
    url = f"{BASE_URL}/messages/{ticket_id}"

    fecha_programada = datetime.now() + timedelta(days=DIAS_A_SUMAR_PROGRAMADO2)
    fecha_programada = fecha_programada.replace(
        hour=HORA_ENVIO_PROGRAMADO2,
        minute=0,
        second=0,
        microsecond=0
    )

    payload = {
        "body": texto,
        "fromMe": True,
        "isNote": False,
        "scheduleDate": fecha_programada.isoformat() + "Z",
        "signMessage": False
    }

    response = requests.post(url, json=payload, headers=HEADERS)
    print(f"Mensaje 2 programado → {response.status_code}")

# FLUJO PRINCIPAL =========================

tag_id, fecha_texto = obtener_tag_y_fecha() #Se obtiene el tag y fecha

if not tag_id:
    print("No existe el tag correspondiente al día:", fecha_texto)
    exit()
queue_id = obtener_queue_id()

if not queue_id:
    print("No existe el departamento:", NOMBRE_QUEUE)
    exit()
tickets = obtener_tickets(queue_id, tag_id)

print("\nTickets encontrados:", len(tickets)) #Mostrar tickets activos

for ticket in tickets:
    ticket_id = ticket["id"]
    nombre_contacto = ticket["contact"]["name"]

    mensaje_inmediato, mensaje_programado1, mensaje_programado2 = (
    MENSAJE_INMEDIATO.format(nombre=nombre_contacto,fecha=fecha_texto),   
    MENSAJE_PROGRAMADO1.format(nombre=nombre_contacto),
    MENSAJE_PROGRAMADO2.format(nombre=nombre_contacto)
)

    enviar_mensaje(ticket_id, mensaje_inmediato)
    programar_mensaje1(ticket_id, mensaje_programado1)
    programar_mensaje2(ticket_id, mensaje_programado2)