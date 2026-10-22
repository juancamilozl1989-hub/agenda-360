"""
Pruebas de unidad del motor de conversación del bot de WhatsApp
(app/services/bot_service.py). Se llama directamente a procesar_mensaje
con una sesión de base de datos; no se envía nada a WhatsApp.

El reloj del servidor se fija en hoy a las 07:00 y los dos barberos
atienden todos los días de 08:00 a 20:00.
"""
import json
from datetime import date, datetime, time, timedelta

import pytest

from app.models.appointment_model import Appointment
from app.models.barber_model import Barber
from app.models.barbershop_model import Barbershop
from app.models.client_model import Client
from app.models.conversation_model import Conversation
from app.models.schedule_model import Schedule
from app.models.service_model import Service
from app.services import appointment_service, bot_service
from app.utils.agenda import DIAS_SEMANA
from app.whatsapp import cliente as whatsapp

pytestmark = pytest.mark.unit

HOY = date.today()
TEL = "573001234567"  # así envía WhatsApp el número (con indicativo)


@pytest.fixture()
def barberia(db, monkeypatch):
    momento = datetime.combine(HOY, time(7, 0))
    monkeypatch.setattr(appointment_service, "ahora", lambda: momento)

    b = Barbershop(nombre="Barbería Central", direccion="x", telefono="1", email="c@c.com")
    db.add(b)
    db.commit()
    andres = Barber(nombre="Andrés López", telefono="1", especialidad="Fade", barbershop_id=b.id)
    sebas = Barber(nombre="Sebastián Gómez", telefono="2", especialidad="Barba", barbershop_id=b.id)
    db.add_all([andres, sebas])
    db.commit()
    corte = Service(nombre="Corte Clásico", categoria="Corte", descripcion="x", precio=25000,
                    duracion=30, barbershop_id=b.id)
    barba = Service(nombre="Barba Premium", categoria="Barba", descripcion="x", precio=18000,
                    duracion=25, barbershop_id=b.id)
    carlos = Client(nombre="Carlos Gómez", telefono="3001234567", email="c@x.com", barbershop_id=b.id)
    db.add_all([corte, barba, carlos])
    db.add_all([
        Schedule(dia_semana=d, hora_inicio=time(8, 0), hora_fin=time(20, 0), barber_id=x.id)
        for x in (andres, sebas) for d in DIAS_SEMANA
    ])
    db.commit()
    # Los menús se ordenan alfabéticamente: servicios 1=Barba Premium, 2=Corte Clásico;
    # barberos 1=cualquiera, 2=Andrés, 3=Sebastián
    return {"barberia": b, "andres": andres, "sebas": sebas, "corte": corte, "carlos": carlos}


def conversar(db, *mensajes, tel=TEL):
    """Envía varios mensajes seguidos y devuelve las respuestas del último."""
    respuestas = []
    for m in mensajes:
        respuestas = bot_service.procesar_mensaje(tel, m, db)
    return "\n".join(respuestas)


def test_saludo_muestra_el_menu(db, barberia):
    r = conversar(db, "hola")
    assert "Barbería Central" in r
    assert "1. Agendar una cita" in r
    assert "Carlos" in r  # reconoce al cliente por su número


def test_cliente_conocido_agenda_una_cita(db, barberia):
    r = conversar(db, "hola", "1", "2", "2", "1", "1")
    assert "Confirma tu cita" in r and "Andrés López" in r and "08:00" in r

    r = conversar(db, "1")
    assert "quedó agendada" in r
    cita = db.query(Appointment).one()
    assert cita.client_id == barberia["carlos"].id
    assert cita.barber_id == barberia["andres"].id
    assert cita.service_id == barberia["corte"].id
    assert (cita.fecha, cita.hora, cita.estado) == (HOY, time(8, 0), "Pendiente")


def test_cliente_nuevo_queda_registrado(db, barberia):
    nuevo = "573119998877"
    r = conversar(db, "hola", "1", tel=nuevo)
    assert "nombre" in r
    r = conversar(db, "laura pérez", tel=nuevo)
    assert "Laura" in r and "¿Qué servicio quieres?" in r
    laura = db.query(Client).filter(Client.nombre == "Laura Pérez").one()
    assert laura.telefono == "3119998877"  # se guarda sin indicativo, como en el panel


def test_horas_ocupadas_no_se_ofrecen(db, barberia):
    db.add(Appointment(fecha=HOY, hora=time(8, 0), client_id=barberia["carlos"].id,
                       barber_id=barberia["andres"].id, service_id=barberia["corte"].id))
    db.commit()
    r = conversar(db, "hola", "1", "2", "2", "1")
    assert "1. 08:30" in r
    assert "08:00" not in r


def test_cualquier_barbero_asigna_uno_libre(db, barberia):
    db.add(Appointment(fecha=HOY, hora=time(8, 0), client_id=barberia["carlos"].id,
                       barber_id=barberia["andres"].id, service_id=barberia["corte"].id))
    db.commit()
    r = conversar(db, "hola", "1", "2", "1", "1", "1")
    assert "08:00" in r and "Sebastián Gómez" in r  # Andrés está ocupado a esa hora


def test_barbero_sin_horario_no_tiene_dias(db, barberia):
    juan = Barber(nombre="Juan Rojas", telefono="3", especialidad="Color",
                  barbershop_id=barberia["barberia"].id)
    db.add(juan)
    db.commit()
    # barberos: 1=cualquiera, 2=Andrés, 3=Juan, 4=Sebastián
    r = conversar(db, "hola", "1", "2", "3")
    assert "No hay horas libres en los próximos" in r


def test_solo_se_ofrecen_dias_con_espacio(db, barberia):
    """Un barbero que atiende un solo día de la semana: solo aparece ese día."""
    juan = Barber(nombre="Juan Rojas", telefono="3", especialidad="Color",
                  barbershop_id=barberia["barberia"].id)
    db.add(juan)
    db.commit()
    dia = HOY + timedelta(days=2)
    db.add(Schedule(dia_semana=DIAS_SEMANA[dia.weekday()], hora_inicio=time(10, 0),
                    hora_fin=time(12, 0), barber_id=juan.id))
    db.commit()
    r = conversar(db, "hola", "1", "2", "3")
    lista = r.split("espacio:")[1]
    assert f"1. {bot_service._fecha_corta(dia)} (4 horas libres)" in lista
    assert f"2. {bot_service._fecha_corta(dia + timedelta(days=7))}" in lista  # la semana siguiente
    assert "3." not in lista


def test_ver_mas_horas(db, barberia):
    # Corte de 30 min de 08:00 a 20:00: 24 horas libres, 12 por página
    r = conversar(db, "hola", "1", "2", "2", "1")
    assert "12. 13:30" in r and "13. Ver más horas" in r
    r = conversar(db, "13")
    assert "1. 14:00" in r and "Ver más horas" not in r
    r = conversar(db, "1")
    assert "Hora: 14:00" in r

def test_respuesta_invalida_pide_el_numero(db, barberia):
    r = conversar(db, "hola", "1", "quiero un corte")
    assert "número del servicio" in r


def test_cero_en_las_horas_vuelve_a_las_fechas(db, barberia):
    r = conversar(db, "hola", "1", "2", "2", "1", "0")
    assert "¿Para qué día?" in r


def test_menu_reinicia_la_conversacion(db, barberia):
    conversar(db, "hola", "1", "2")
    r = conversar(db, "menú")
    assert "1. Agendar una cita" in r
    conv = db.query(Conversation).filter(Conversation.telefono == TEL).one()
    assert conv.paso == "menu" and json.loads(conv.datos) == {}


def test_hora_tomada_mientras_confirmaba(db, barberia):
    conversar(db, "hola", "1", "2", "2", "1", "1")  # elige 08:00 con Andrés
    # Otra persona toma esa hora antes de que confirme
    db.add(Appointment(fecha=HOY, hora=time(8, 0), client_id=barberia["carlos"].id,
                       barber_id=barberia["andres"].id, service_id=barberia["corte"].id))
    db.commit()
    r = conversar(db, "1")
    assert "se cruza" in r
    assert "Estas son las horas libres" in r
    assert db.query(Appointment).count() == 1


def test_mis_citas_y_visitas(db, barberia):
    c = barberia["carlos"]
    db.add_all([
        Appointment(fecha=HOY + timedelta(days=1), hora=time(9, 0), client_id=c.id,
                    barber_id=barberia["andres"].id, service_id=barberia["corte"].id),
        Appointment(fecha=HOY - timedelta(days=3), hora=time(9, 0), estado="Completada", client_id=c.id,
                    barber_id=barberia["andres"].id, service_id=barberia["corte"].id),
    ])
    db.commit()
    r = conversar(db, "hola", "2")
    assert "Tus próximas citas" in r and "09:00" in r
    assert "Llevas 1 visita" in r


def test_cancelar_una_cita(db, barberia):
    cita = Appointment(fecha=HOY + timedelta(days=1), hora=time(9, 0), client_id=barberia["carlos"].id,
                       barber_id=barberia["andres"].id, service_id=barberia["corte"].id)
    db.add(cita)
    db.commit()
    r = conversar(db, "hola", "3")
    assert "¿Cuál cita quieres cancelar?" in r
    r = conversar(db, "1")
    assert "quedó cancelada" in r
    db.refresh(cita)
    assert cita.estado == "Cancelada"


def test_conversacion_inactiva_vuelve_a_empezar(db, barberia, monkeypatch):
    conversar(db, "hola", "1", "2")  # queda en el paso de barbero
    despues = datetime.combine(HOY, time(9, 0))
    monkeypatch.setattr(appointment_service, "ahora", lambda: despues)
    r = conversar(db, "2")  # "2" ya no es un barbero sino la opción del menú
    assert "No tienes citas próximas" in r


def test_numero_de_whatsapp_a_telefono_local():
    assert bot_service.telefono_local("573001234567") == "3001234567"
    assert bot_service.telefono_local("+57 300 123 4567") == "3001234567"


# ---------------------------------------------------------------
# Envío de mensajes a la API de Meta
# ---------------------------------------------------------------
def test_sin_credenciales_no_se_envia(monkeypatch):
    monkeypatch.setattr(whatsapp.config, "WHATSAPP_TOKEN", "")
    assert whatsapp.enviar_texto(TEL, "hola") is False


def test_envio_arma_la_peticion_a_meta(monkeypatch):
    monkeypatch.setattr(whatsapp.config, "WHATSAPP_TOKEN", "token-de-prueba")
    monkeypatch.setattr(whatsapp.config, "WHATSAPP_PHONE_NUMBER_ID", "123456")
    llamada = {}

    class Respuesta:
        status_code = 200
        text = "{}"

    def falso_post(url, json, headers, timeout):
        llamada.update(url=url, json=json, headers=headers)
        return Respuesta()

    monkeypatch.setattr(whatsapp.httpx, "post", falso_post)
    assert whatsapp.enviar_texto(TEL, "hola") is True
    assert llamada["url"].endswith("/123456/messages")
    assert llamada["json"]["to"] == TEL and llamada["json"]["text"]["body"] == "hola"
    assert llamada["headers"]["Authorization"] == "Bearer token-de-prueba"


# ---------------------------------------------------------------
# Respuestas inesperadas del cliente
# ---------------------------------------------------------------
def test_confirmacion_con_respuesta_invalida_y_no_agendar(db, barberia):
    r = conversar(db, "hola", "1", "2", "2", "1", "1", "tal vez")
    assert "Responde *1* para confirmar" in r
    r = conversar(db, "2")
    assert "no agendé nada" in r
    assert db.query(Appointment).count() == 0


def test_nombre_invalido_se_vuelve_a_pedir(db, barberia):
    r = conversar(db, "hola", "1", "12", tel="573110000000")
    assert "nombre y apellido" in r


def test_cancelar_sin_citas_y_desistir(db, barberia):
    assert "No tienes citas próximas para cancelar" in conversar(db, "hola", "3")
    db.add(Appointment(fecha=HOY + timedelta(days=1), hora=time(9, 0), client_id=barberia["carlos"].id,
                       barber_id=barberia["andres"].id, service_id=barberia["corte"].id))
    db.commit()
    assert "no cancelé ninguna" in conversar(db, "hola", "3", "0")


def test_sin_servicios_activos(db, barberia):
    for s in db.query(Service).all():
        s.estado = "Inactivo"
    db.commit()
    assert "no hay servicios disponibles" in conversar(db, "hola", "1")


def test_numero_desconocido_no_tiene_citas(db, barberia):
    assert "Todavía no tienes citas" in conversar(db, "hola", "2", tel="573110000000")


def test_error_de_conexion_con_meta(monkeypatch):
    monkeypatch.setattr(whatsapp.config, "WHATSAPP_TOKEN", "t")
    monkeypatch.setattr(whatsapp.config, "WHATSAPP_PHONE_NUMBER_ID", "1")

    def falla(*a, **k):
        raise whatsapp.httpx.ConnectError("sin red")

    monkeypatch.setattr(whatsapp.httpx, "post", falla)
    assert whatsapp.enviar_texto(TEL, "hola") is False


def test_meta_rechaza_el_mensaje(monkeypatch):
    monkeypatch.setattr(whatsapp.config, "WHATSAPP_TOKEN", "t")
    monkeypatch.setattr(whatsapp.config, "WHATSAPP_PHONE_NUMBER_ID", "1")

    class Rechazo:
        status_code = 401
        text = '{"error": "token vencido"}'

    monkeypatch.setattr(whatsapp.httpx, "post", lambda *a, **k: Rechazo())
    assert whatsapp.enviar_texto(TEL, "hola") is False
