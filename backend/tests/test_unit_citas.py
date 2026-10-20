"""
Pruebas unitarias de la regla de negocio de citas
(app/services/appointment_service.py), ejecutadas directamente
sobre una sesión de base de datos, sin pasar por HTTP.
"""
from datetime import date, datetime, time, timedelta

import pytest
from fastapi import HTTPException

from app.models.barber_model import Barber
from app.models.barbershop_model import Barbershop
from app.models.client_model import Client
from app.models.schedule_model import Schedule
from app.models.service_model import Service
from app.utils.agenda import DIAS_SEMANA
from app.schemas.appointment_schema import AppointmentCreate
from app.services import appointment_service

pytestmark = pytest.mark.unit

MANANA = date.today() + timedelta(days=1)


@pytest.fixture()
def escenario(db):
    """
    Barbería, dos barberos que atienden todos los días de 08:00 a
    20:00, un servicio de 30 minutos del catálogo y un cliente.
    """
    barberia = Barbershop(
        nombre="Central", direccion="Cll 1", telefono="300", email="c@c.com"
    )
    db.add(barberia)
    db.commit()

    b1 = Barber(nombre="Andrés", telefono="1", especialidad="Fade", barbershop_id=barberia.id)
    b2 = Barber(nombre="Sebastián", telefono="2", especialidad="Barba", barbershop_id=barberia.id)
    cliente = Client(nombre="Carlos", telefono="3", email="c@x.com", barbershop_id=barberia.id)
    db.add_all([b1, b2, cliente])
    db.commit()

    servicio = Service(
        nombre="Corte", categoria="Corte", descripcion="Corte", precio=25000,
        duracion=30, barbershop_id=barberia.id,
    )
    db.add(servicio)
    db.add_all([
        Schedule(dia_semana=dia, hora_inicio=time(8, 0), hora_fin=time(20, 0), barber_id=b.id)
        for b in (b1, b2)
        for dia in DIAS_SEMANA
    ])
    db.commit()

    return {"b1": b1, "b2": b2, "cliente": cliente, "servicio": servicio, "barberia": barberia}


def _datos(e, **cambios):
    base = dict(
        fecha=MANANA,
        hora=time(9, 0),
        client_id=e["cliente"].id,
        barber_id=e["b1"].id,
        service_id=e["servicio"].id,
    )
    base.update(cambios)
    return AppointmentCreate(**base)


def test_crea_cita_valida_con_estado_pendiente(db, escenario):
    cita = appointment_service.crear_cita(_datos(escenario), db)
    assert cita.id is not None
    assert cita.estado == "Pendiente"


def test_rechaza_fecha_pasada(db, escenario):
    ayer = date.today() - timedelta(days=1)
    with pytest.raises(HTTPException) as error:
        appointment_service.crear_cita(_datos(escenario, fecha=ayer), db)
    assert error.value.status_code == 400
    assert "fechas pasadas" in error.value.detail


def _fijar_hora(monkeypatch, hora: time):
    """Simula que el reloj del servidor marca hoy a la hora indicada."""
    momento = datetime.combine(date.today(), hora)
    monkeypatch.setattr(appointment_service, "ahora", lambda: momento)


def test_acepta_cita_para_hoy(db, escenario, monkeypatch):
    _fijar_hora(monkeypatch, time(8, 0))  # son las 8:00, la cita es a las 9:00
    cita = appointment_service.crear_cita(_datos(escenario, fecha=date.today()), db)
    assert cita.id is not None


def test_rechaza_hora_pasada_del_dia_de_hoy(db, escenario, monkeypatch):
    _fijar_hora(monkeypatch, time(22, 50))  # ya es de noche
    with pytest.raises(HTTPException) as error:
        appointment_service.crear_cita(
            _datos(escenario, fecha=date.today(), hora=time(9, 0)), db
        )
    assert error.value.status_code == 400
    assert "hora que ya pasó" in error.value.detail


def test_cliente_inexistente(db, escenario):
    with pytest.raises(HTTPException) as error:
        appointment_service.crear_cita(_datos(escenario, client_id=999), db)
    assert error.value.status_code == 404
    assert error.value.detail == "Cliente no encontrado"


def test_barbero_inexistente(db, escenario):
    with pytest.raises(HTTPException) as error:
        appointment_service.crear_cita(_datos(escenario, barber_id=999), db)
    assert error.value.status_code == 404
    assert error.value.detail == "Barbero no encontrado"


def test_servicio_inexistente(db, escenario):
    with pytest.raises(HTTPException) as error:
        appointment_service.crear_cita(_datos(escenario, service_id=999), db)
    assert error.value.status_code == 404
    assert error.value.detail == "Servicio no encontrado"


def test_cualquier_barbero_atiende_cualquier_servicio(db, escenario):
    cita = appointment_service.crear_cita(
        _datos(escenario, barber_id=escenario["b2"].id), db
    )
    assert cita.barber_id == escenario["b2"].id


def test_rechaza_cita_duplicada_del_mismo_barbero(db, escenario):
    appointment_service.crear_cita(_datos(escenario), db)
    with pytest.raises(HTTPException) as error:
        appointment_service.crear_cita(_datos(escenario), db)
    assert error.value.status_code == 400
    assert "ya tiene una cita" in error.value.detail


def test_misma_hora_en_otro_dia_si_se_permite(db, escenario):
    appointment_service.crear_cita(_datos(escenario), db)
    otra = appointment_service.crear_cita(
        _datos(escenario, fecha=MANANA + timedelta(days=1)), db
    )
    assert otra.id is not None


def test_otra_hora_el_mismo_dia_si_se_permite(db, escenario):
    appointment_service.crear_cita(_datos(escenario), db)
    otra = appointment_service.crear_cita(_datos(escenario, hora=time(10, 0)), db)
    assert otra.id is not None


def test_cita_cancelada_no_ocupa_el_horario(db, escenario):
    """Hallazgo H-01: una cita cancelada debe liberar el horario del barbero."""
    primera = appointment_service.crear_cita(_datos(escenario), db)
    primera.estado = "Cancelada"
    db.commit()

    nueva = appointment_service.crear_cita(_datos(escenario), db)
    assert nueva.id is not None
    assert nueva.id != primera.id
    assert nueva.estado == "Pendiente"


# ---------------------------------------------------------------
# Reglas de agenda: horario del barbero y duración del servicio
# ---------------------------------------------------------------
def test_rechaza_cita_fuera_del_horario_del_barbero(db, escenario):
    with pytest.raises(HTTPException) as error:
        appointment_service.crear_cita(_datos(escenario, hora=time(7, 0)), db)
    assert error.value.status_code == 400
    assert "fuera del horario" in error.value.detail


def test_rechaza_cruce_teniendo_en_cuenta_la_duracion(db, escenario):
    appointment_service.crear_cita(_datos(escenario, hora=time(9, 0)), db)  # 9:00-9:30
    with pytest.raises(HTTPException) as error:
        appointment_service.crear_cita(_datos(escenario, hora=time(9, 15)), db)
    assert error.value.status_code == 400
    assert "ya tiene una cita" in error.value.detail


def test_rechaza_barbero_inactivo(db, escenario):
    escenario["b1"].estado = "Inactivo"
    db.commit()
    with pytest.raises(HTTPException) as error:
        appointment_service.crear_cita(_datos(escenario), db)
    assert error.value.status_code == 400
    assert "no está activo" in error.value.detail
