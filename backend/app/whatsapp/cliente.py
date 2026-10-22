"""
Envío de mensajes por la WhatsApp Cloud API de Meta.

Si el token o el identificador del número no están configurados,
el mensaje solo se escribe en el registro (útil en desarrollo y pruebas).
"""
import logging

import httpx

from app.core import config

logger = logging.getLogger("agenda360.whatsapp")


def esta_configurado() -> bool:
    """True si hay credenciales para enviar mensajes reales."""
    return bool(config.WHATSAPP_TOKEN and config.WHATSAPP_PHONE_NUMBER_ID)


def enviar_texto(telefono: str, texto: str) -> bool:
    """
    Envía un mensaje de texto a un número de WhatsApp.
    Devuelve True si Meta lo aceptó.
    """
    if not esta_configurado():
        logger.warning("WhatsApp sin configurar. Mensaje para %s:\n%s", telefono, texto)
        return False

    url = (
        f"https://graph.facebook.com/{config.WHATSAPP_API_VERSION}/"
        f"{config.WHATSAPP_PHONE_NUMBER_ID}/messages"
    )
    cuerpo = {
        "messaging_product": "whatsapp",
        "to": telefono,
        "type": "text",
        "text": {"preview_url": False, "body": texto},
    }

    try:
        respuesta = httpx.post(
            url,
            json=cuerpo,
            headers={"Authorization": f"Bearer {config.WHATSAPP_TOKEN}"},
            timeout=15,
        )
    except httpx.HTTPError as error:
        logger.error("No se pudo conectar con WhatsApp: %s", error)
        return False

    if respuesta.status_code >= 400:
        logger.error("WhatsApp rechazó el mensaje (%s): %s", respuesta.status_code, respuesta.text)
        return False

    return True
