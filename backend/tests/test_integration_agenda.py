"""
Pruebas de integración de las reglas de agenda y de la consulta de
disponibilidad (GET /availability/), que es la base del bot de WhatsApp.

En los datos de apoyo ambos barberos atienden todos los días de 08:00
a 20:00 y el servicio "Corte Clásico" dura 30 minutos.
"""
from datetime import date, datetime, time

import pytest

from app.services import appointment_service
from tests.conftest import ayer, cuerpo_cita, manana

pytestmark = pytest.mark.integration


def _fijar_hora(monkeypatch, hora: time):
    """Simula que el reloj del servidor marca hoy a la hora indicada."""
    momento = datetime.combine(date.today(), hora)
    monkeypatch.setattr(appointment_service, "ahora", lambda: momento)


def _barbero_sin_horario(client, h, datos):
    return client.post(
        "/barbers/", headers=h,
        json={"nombre": "Juan Rojas", "telefono": "300", "especialidad": "Color",
              "barbershop_id": datos["barberia_id"]},
    ).json()["id"]


def _servicio(client, h, datos, nombre="Corte + Barba", duracion=50, estado="Activo"):
    return client.post(
        "/services/", headers=h,
        json={"nombre": nombre, "categoria": "Corte", "descripcion": nombre,
              "precio": 38000, "duracion": duracion, "estado": estado,
              "barbershop_id": datos["barberia_id"]},
    ).json()["id"]


def _disponibilidad(client, h, datos, fecha=None, barber_id=None, service_id=None):
    params = {"fecha": fecha or manana(),
              "service_id": service_id or datos["servicio_id"]}
    if barber_id is not None:
        params["barber_id"] = barber_id
    return client.get("/availability/", headers=h, params=params)


def _horas(respuesta) -> list[str]:
    return [d["hora"][:5] for d in respuesta.json()["disponibles"]]


# ---------------------------------------------------------------
# Reglas de agenda al registrar citas
# ---------------------------------------------------------------
def test_cita_antes_de_abrir_es_rechazada(client, auth_headers, datos):
    r = client.post("/appointments/", headers=auth_headers, json=cuerpo_cita(datos, hora="07:00"))
    assert r.status_code == 400
    assert "fuera del horario" in r.json()["detail"]


def test_servicio_que_termina_despues_del_cierre(client, auth_headers, datos):
    # Empieza 19:45 y dura 30 minutos: terminaría 20:15, después del cierre
    r = client.post("/appointments/", headers=auth_headers, json=cuerpo_cita(datos, hora="19:45"))
    assert r.status_code == 400
    assert "fuera del horario" in r.json()["detail"]


def test_ultimo_turno_que_cabe_es_aceptado(client, auth_headers, datos):
    r = client.post("/appointments/", headers=auth_headers, json=cuerpo_cita(datos, hora="19:30"))
    assert r.status_code == 200


def test_barbero_sin_horario_ese_dia(client, auth_headers, datos):
    h = auth_headers
    cuerpo = cuerpo_cita(datos)
    cuerpo["barber_id"] = _barbero_sin_horario(client, h, datos)
    r = client.post("/appointments/", headers=h, json=cuerpo)
    assert r.status_code == 400
    assert "no atiende" in r.json()["detail"]


def test_cruce_por_duracion_es_rechazado(client, auth_headers, datos):
    h = auth_headers
    largo = _servicio(client, h, datos, duracion=50)  # 09:00 a 09:50

    primera = cuerpo_cita(datos, hora="09:00")
    primera["service_id"] = largo
    assert client.post("/appointments/", headers=h, json=primera).status_code == 200

    # 09:30 se cruza con la cita de 09:00 que termina 09:50
    r = client.post("/appointments/", headers=h, json=cuerpo_cita(datos, hora="09:30"))
    assert r.status_code == 400
    assert "ya tiene una cita" in r.json()["detail"]

    # 10:00 ya está libre
    assert client.post("/appointments/", headers=h,
                       json=cuerpo_cita(datos, hora="10:00")).status_code == 200


def test_barbero_inactivo_no_recibe_citas(client, auth_headers, datos):
    h = auth_headers
    client.put(f"/barbers/{datos['barbero_id']}", headers=h,
               json={"nombre": "Andrés López", "telefono": "3001234567",
                     "especialidad": "Fade", "estado": "Inactivo",
                     "barbershop_id": datos["barberia_id"]})
    r = client.post("/appointments/", headers=h, json=cuerpo_cita(datos))
    assert r.status_code == 400
    assert "no está activo" in r.json()["detail"]


def test_servicio_inactivo_no_se_puede_agendar(client, auth_headers, datos):
    h = auth_headers
    inactivo = _servicio(client, h, datos, nombre="Color", estado="Inactivo")
    cuerpo = cuerpo_cita(datos)
    cuerpo["service_id"] = inactivo
    r = client.post("/appointments/", headers=h, json=cuerpo)
    assert r.status_code == 400
    assert "no está activo" in r.json()["detail"]


def test_cita_existente_se_puede_completar_aunque_cambie_el_horario(client, auth_headers, datos):
    """Cambiar solo el estado no vuelve a exigir el horario del barbero."""
    h = auth_headers
    cita = client.post("/appointments/", headers=h, json=cuerpo_cita(datos, hora="09:00")).json()

    # El barbero deja de atender todos los días
    for horario in client.get("/schedules/", headers=h).json():
        if horario["barber"]["id"] == datos["barbero_id"]:
            client.delete(f"/schedules/{horario['id']}", headers=h)

    cuerpo = cuerpo_cita(datos, hora="09:00")
    cuerpo["estado"] = "Completada"
    r = client.put(f"/appointments/{cita['id']}", headers=h, json=cuerpo)
    assert r.status_code == 200

    # Pero reprogramarla sí exige el horario
    cuerpo = cuerpo_cita(datos, hora="10:00")
    cuerpo["estado"] = "Pendiente"
    assert client.put(f"/appointments/{cita['id']}", headers=h, json=cuerpo).status_code == 400


# ---------------------------------------------------------------
# Disponibilidad
# ---------------------------------------------------------------
def test_disponibilidad_de_un_barbero(client, auth_headers, datos):
    r = _disponibilidad(client, auth_headers, datos, barber_id=datos["barbero_id"])
    assert r.status_code == 200
    cuerpo = r.json()
    horas = _horas(r)

    # De 08:00 a 19:30 cada 30 minutos: 24 turnos
    assert len(horas) == 24
    assert horas[0] == "08:00" and horas[-1] == "19:30"
    assert cuerpo["servicio"]["duracion"] == 30
    assert all(d["barberos"] == [{"id": datos["barbero_id"], "nombre": "Andrés López"}]
               for d in cuerpo["disponibles"])


def test_disponibilidad_excluye_horas_ocupadas(client, auth_headers, datos):
    h = auth_headers
    client.post("/appointments/", headers=h, json=cuerpo_cita(datos, hora="09:00"))

    horas = _horas(_disponibilidad(client, h, datos, barber_id=datos["barbero_id"]))
    assert "09:00" not in horas
    assert "08:30" in horas and "09:30" in horas


def test_disponibilidad_sin_barbero_indica_quien_esta_libre(client, auth_headers, datos):
    h = auth_headers
    client.post("/appointments/", headers=h, json=cuerpo_cita(datos, hora="09:00"))

    r = _disponibilidad(client, h, datos)
    nueve = next(d for d in r.json()["disponibles"] if d["hora"].startswith("09:00"))
    assert [b["id"] for b in nueve["barberos"]] == [datos["otro_barbero_id"]]

    diez = next(d for d in r.json()["disponibles"] if d["hora"].startswith("10:00"))
    assert len(diez["barberos"]) == 2


def test_cita_cancelada_vuelve_a_estar_disponible(client, auth_headers, datos):
    h = auth_headers
    cita = client.post("/appointments/", headers=h, json=cuerpo_cita(datos, hora="09:00")).json()
    cuerpo = cuerpo_cita(datos, hora="09:00")
    cuerpo["estado"] = "Cancelada"
    client.put(f"/appointments/{cita['id']}", headers=h, json=cuerpo)

    horas = _horas(_disponibilidad(client, h, datos, barber_id=datos["barbero_id"]))
    assert "09:00" in horas


def test_disponibilidad_tiene_en_cuenta_la_duracion(client, auth_headers, datos):
    h = auth_headers
    largo = _servicio(client, h, datos, duracion=50)
    client.post("/appointments/", headers=h, json=cuerpo_cita(datos, hora="09:00"))  # 09:00-09:30

    horas = _horas(_disponibilidad(client, h, datos, barber_id=datos["barbero_id"],
                                   service_id=largo))
    assert "08:00" in horas          # 08:00-08:50 cabe
    assert "08:30" not in horas      # 08:30-09:20 se cruza
    assert "09:30" in horas
    assert horas[-1] == "19:00"      # 19:30-20:20 pasaría del cierre


def test_disponibilidad_de_hoy_omite_horas_pasadas(client, auth_headers, datos, monkeypatch):
    _fijar_hora(monkeypatch, time(12, 10))
    horas = _horas(_disponibilidad(client, auth_headers, datos, fecha=date.today().isoformat(),
                                   barber_id=datos["barbero_id"]))
    assert horas[0] == "12:30"


def test_disponibilidad_de_barbero_sin_horario_esta_vacia(client, auth_headers, datos):
    h = auth_headers
    bid = _barbero_sin_horario(client, h, datos)
    r = _disponibilidad(client, h, datos, barber_id=bid)
    assert r.status_code == 200
    assert r.json()["disponibles"] == []


def test_disponibilidad_con_datos_invalidos(client, auth_headers, datos):
    h = auth_headers
    assert _disponibilidad(client, h, datos, service_id=999).status_code == 404
    assert _disponibilidad(client, h, datos, barber_id=999).status_code == 404
    assert _disponibilidad(client, h, datos, fecha=ayer()).status_code == 400


def test_disponibilidad_requiere_token(client, datos):
    r = client.get("/availability/", params={"fecha": manana(), "service_id": datos["servicio_id"]})
    assert r.status_code == 401


def test_cita_en_una_hora_ofrecida_siempre_se_acepta(client, auth_headers, datos):
    """Lo que ofrece la disponibilidad debe poder agendarse (flujo del bot)."""
    h = auth_headers
    r = _disponibilidad(client, h, datos)
    primera = r.json()["disponibles"][0]

    cuerpo = cuerpo_cita(datos, hora=primera["hora"][:5])
    cuerpo["barber_id"] = primera["barberos"][0]["id"]
    assert client.post("/appointments/", headers=h, json=cuerpo).status_code == 200
