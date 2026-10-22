"""
Pruebas de integración del webhook de WhatsApp (/webhook/whatsapp).
Se simulan las notificaciones que envía Meta; las respuestas del bot se
capturan en una lista en lugar de enviarse a WhatsApp.
"""
import hashlib
import hmac
import json

import pytest

from app.core import config
from app.whatsapp import cliente as whatsapp

pytestmark = pytest.mark.integration

URL = "/webhook/whatsapp"


@pytest.fixture()
def enviados(monkeypatch):
    lista = []
    monkeypatch.setattr(whatsapp, "enviar_texto", lambda tel, texto: lista.append((tel, texto)) or True)
    return lista


def notificacion(texto="hola", telefono="573001234567", mensaje_id="wamid.1"):
    """Cuerpo con la misma forma que usa la WhatsApp Cloud API."""
    return {
        "object": "whatsapp_business_account",
        "entry": [{"id": "1", "changes": [{"field": "messages", "value": {
            "messaging_product": "whatsapp",
            "contacts": [{"wa_id": telefono, "profile": {"name": "Carlos"}}],
            "messages": [{"from": telefono, "id": mensaje_id, "timestamp": "1",
                          "type": "text", "text": {"body": texto}}],
        }}]}],
    }


def test_verificacion_del_webhook(client, monkeypatch):
    monkeypatch.setattr(config, "WHATSAPP_VERIFY_TOKEN", "mi-token")
    r = client.get(URL, params={"hub.mode": "subscribe", "hub.verify_token": "mi-token",
                                "hub.challenge": "12345"})
    assert r.status_code == 200
    assert r.text == "12345"


def test_verificacion_con_token_incorrecto(client, monkeypatch):
    monkeypatch.setattr(config, "WHATSAPP_VERIFY_TOKEN", "mi-token")
    r = client.get(URL, params={"hub.mode": "subscribe", "hub.verify_token": "otro",
                                "hub.challenge": "12345"})
    assert r.status_code == 403


def test_mensaje_recibe_respuesta_sin_token_jwt(client, datos, enviados):
    r = client.post(URL, json=notificacion("hola"))
    assert r.status_code == 200
    assert r.json() == {"procesados": 1}
    assert enviados[0][0] == "573001234567"
    assert "Agendar una cita" in enviados[0][1]


def test_mensaje_duplicado_se_procesa_una_vez(client, datos, enviados):
    client.post(URL, json=notificacion("hola", mensaje_id="wamid.repetido"))
    r = client.post(URL, json=notificacion("hola", mensaje_id="wamid.repetido"))
    assert r.json() == {"procesados": 0}
    assert len(enviados) == 1


def test_notificaciones_de_estado_se_ignoran(client, enviados):
    estado = {"entry": [{"changes": [{"value": {"statuses": [{"id": "x", "status": "read"}]}}]}]}
    r = client.post(URL, json=estado)
    assert r.json() == {"procesados": 0}
    assert enviados == []


def test_firma_invalida_es_rechazada(client, monkeypatch, enviados):
    monkeypatch.setattr(config, "WHATSAPP_APP_SECRET", "secreto")
    r = client.post(URL, json=notificacion(), headers={"X-Hub-Signature-256": "sha256=falsa"})
    assert r.status_code == 403
    assert enviados == []


def test_firma_valida_es_aceptada(client, datos, monkeypatch, enviados):
    monkeypatch.setattr(config, "WHATSAPP_APP_SECRET", "secreto")
    cuerpo = json.dumps(notificacion()).encode()
    firma = hmac.new(b"secreto", cuerpo, hashlib.sha256).hexdigest()
    r = client.post(URL, content=cuerpo, headers={"X-Hub-Signature-256": f"sha256={firma}",
                                                  "Content-Type": "application/json"})
    assert r.status_code == 200
    assert len(enviados) == 1


def test_agendamiento_completo_por_whatsapp(client, auth_headers, datos, enviados):
    """De extremo a extremo: la cita creada por WhatsApp aparece en la API del panel."""
    pasos = ["hola", "1", "1", "2", "2", "1", "1"]  # menú, servicio, barbero, mañana, primera hora, confirmar
    for i, texto in enumerate(pasos):
        client.post(URL, json=notificacion(texto, telefono="573019876543", mensaje_id=f"wamid.{i}"))
    assert "quedó agendada" in enviados[-1][1]

    citas = client.get("/appointments/", headers=auth_headers).json()
    assert len(citas) == 1
    assert citas[0]["client"]["nombre"] == "Carlos Gómez"  # cliente de los datos de apoyo
    assert citas[0]["estado"] == "Pendiente"


def test_json_invalido(client):
    r = client.post(URL, content=b"{no es json", headers={"Content-Type": "application/json"})
    assert r.status_code == 400


def test_firma_ausente_es_rechazada(client, monkeypatch, enviados):
    monkeypatch.setattr(config, "WHATSAPP_APP_SECRET", "secreto")
    assert client.post(URL, json=notificacion()).status_code == 403


def test_imagen_o_audio_responde_con_el_menu(client, datos, enviados):
    cuerpo = notificacion()
    mensaje = cuerpo["entry"][0]["changes"][0]["value"]["messages"][0]
    mensaje["type"] = "image"
    mensaje.pop("text")
    r = client.post(URL, json=cuerpo)
    assert r.json() == {"procesados": 1}
    assert "Agendar una cita" in enviados[0][1]


def test_error_interno_no_deja_al_cliente_sin_respuesta(client, datos, enviados, monkeypatch):
    from app.services import bot_service

    def falla(*a, **k):
        raise RuntimeError("fallo simulado")

    monkeypatch.setattr(bot_service, "procesar_mensaje", falla)
    r = client.post(URL, json=notificacion())
    assert r.status_code == 200
    assert "tuve un problema" in enviados[0][1]
