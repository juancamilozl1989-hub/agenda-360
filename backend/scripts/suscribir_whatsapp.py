"""
Suscribe la app de Meta a la cuenta de WhatsApp Business, para que los
mensajes que llegan al número de prueba se envíen al webhook.

Uso (desde la carpeta backend, con el venv activo):
    python scripts/suscribir_whatsapp.py ID_DE_LA_CUENTA_DE_WHATSAPP_BUSINESS

El token se toma del archivo .env (WHATSAPP_TOKEN), así no hay que escribirlo.
"""
import os
import sys

import httpx
from dotenv import load_dotenv

load_dotenv()

if len(sys.argv) != 2 or not sys.argv[1].isdigit():
    print("Uso: python scripts/suscribir_whatsapp.py ID_DE_LA_CUENTA_DE_WHATSAPP_BUSINESS")
    sys.exit(1)

token = os.getenv("WHATSAPP_TOKEN", "")
version = os.getenv("WHATSAPP_API_VERSION", "v23.0")
if not token:
    print("Falta WHATSAPP_TOKEN en el archivo .env")
    sys.exit(1)

cuenta = sys.argv[1]
respuesta = httpx.post(
    f"https://graph.facebook.com/{version}/{cuenta}/subscribed_apps",
    headers={"Authorization": f"Bearer {token}"},
    timeout=15,
)
print(respuesta.status_code, respuesta.text)
if respuesta.status_code == 200:
    print("Listo: la app quedó suscrita. Escríbele 'hola' al número de prueba.")
