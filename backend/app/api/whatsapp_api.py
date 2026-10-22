"""
Webhook del bot de WhatsApp (WhatsApp Cloud API de Meta).

- GET  /webhook/whatsapp: Meta verifica la URL al configurar el webhook.
- POST /webhook/whatsapp: Meta envía aquí cada mensaje que recibe el número.

Estas rutas no usan el token JWT del panel: Meta no lo tiene. En su lugar
se valida el token de verificación y, si está configurado, la firma
X-Hub-Signature-256 de cada mensaje.
"""
import hashlib
import hmac
import json
import logging

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.core import config
from app.core.dependencies import get_db
from app.models.conversation_model import Conversation
from app.services import bot_service
from app.whatsapp import cliente as whatsapp

logger = logging.getLogger("agenda360.whatsapp")

router = APIRouter(
    prefix="/webhook/whatsapp",
    tags=["Bot de WhatsApp"]
)


# ==========================================
# Verificación del webhook
# ==========================================
@router.get("", response_class=PlainTextResponse)
def verificar_webhook(
    modo: str = Query(None, alias="hub.mode"),
    token: str = Query(None, alias="hub.verify_token"),
    reto: str = Query(None, alias="hub.challenge"),
):
    """
    Meta llama a esta ruta una sola vez al registrar el webhook y espera
    que se le devuelva el valor de hub.challenge si el token coincide.
    """
    if (
        modo == "subscribe"
        and config.WHATSAPP_VERIFY_TOKEN
        and token == config.WHATSAPP_VERIFY_TOKEN
    ):
        return reto or ""

    raise HTTPException(status_code=403, detail="Token de verificación inválido")


# ==========================================
# Firma de los mensajes
# ==========================================
def firma_valida(cuerpo: bytes, firma: str | None) -> bool:
    """
    Comprueba que el mensaje lo envió Meta, usando la clave secreta de la app.
    Si no hay clave configurada (desarrollo), se acepta.
    """
    if not config.WHATSAPP_APP_SECRET:
        return True
    if not firma or not firma.startswith("sha256="):
        return False
    esperada = hmac.new(
        config.WHATSAPP_APP_SECRET.encode(), cuerpo, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(esperada, firma.removeprefix("sha256="))


def extraer_mensajes(payload: dict) -> list[dict]:
    """
    Saca de la notificación de Meta los mensajes de texto recibidos.
    Las notificaciones de estado (enviado, leído...) se ignoran.
    """
    mensajes = []
    for entrada in payload.get("entry", []):
        for cambio in entrada.get("changes", []):
            valor = cambio.get("value", {})
            nombres = {
                c.get("wa_id"): c.get("profile", {}).get("name")
                for c in valor.get("contacts", [])
            }
            for m in valor.get("messages", []):
                if m.get("type") == "text":
                    texto = m.get("text", {}).get("body", "")
                elif m.get("type") == "interactive":
                    interactivo = m.get("interactive", {})
                    texto = (interactivo.get("button_reply") or interactivo.get("list_reply") or {}).get("id", "")
                else:
                    texto = ""  # audios, imágenes...: se responde con el menú
                mensajes.append({
                    "id": m.get("id"),
                    "telefono": m.get("from"),
                    "texto": texto,
                    "nombre": nombres.get(m.get("from")),
                })
    return mensajes


def _enviar_respuestas(telefono: str, respuestas: list[str]):
    for texto in respuestas:
        whatsapp.enviar_texto(telefono, texto)


# ==========================================
# Recepción de mensajes
# ==========================================
@router.post("")
async def recibir_mensajes(
    request: Request,
    tareas: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Procesa los mensajes que llegan al número de WhatsApp y programa el
    envío de las respuestas. Siempre responde 200 rápido, como pide Meta;
    si no lo hace, Meta reintenta el envío.
    """
    cuerpo = await request.body()

    if not firma_valida(cuerpo, request.headers.get("X-Hub-Signature-256")):
        raise HTTPException(status_code=403, detail="Firma inválida")

    try:
        payload = json.loads(cuerpo or b"{}")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="JSON inválido")

    procesados = 0
    for mensaje in extraer_mensajes(payload):
        if not mensaje["telefono"]:
            continue

        # WhatsApp puede reenviar el mismo mensaje: se procesa una sola vez
        conv = db.query(Conversation).filter(
            Conversation.telefono == mensaje["telefono"]
        ).first()
        if conv and mensaje["id"] and conv.ultimo_mensaje_id == mensaje["id"]:
            continue

        try:
            respuestas = bot_service.procesar_mensaje(
                mensaje["telefono"], mensaje["texto"], db, mensaje["nombre"]
            )
        except Exception:
            logger.exception("Error procesando el mensaje de %s", mensaje["telefono"])
            db.rollback()
            respuestas = ["Ups, tuve un problema procesando tu mensaje. Escribe *menú* para intentarlo de nuevo."]

        conv = db.query(Conversation).filter(
            Conversation.telefono == mensaje["telefono"]
        ).first()
        if conv:
            conv.ultimo_mensaje_id = mensaje["id"]
            db.commit()

        tareas.add_task(_enviar_respuestas, mensaje["telefono"], respuestas)
        procesados += 1

    return {"procesados": procesados}
