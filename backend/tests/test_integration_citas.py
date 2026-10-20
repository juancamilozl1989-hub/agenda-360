"""Pruebas de integración del módulo de citas (flujo principal del sistema)."""
import pytest

from tests.conftest import ayer, cuerpo_cita, manana

pytestmark = pytest.mark.integration


def test_crear_cita_valida(client, auth_headers, datos):
    r = client.post("/appointments/", headers=auth_headers, json=cuerpo_cita(datos))
    assert r.status_code == 200
    cita = r.json()
    assert cita["estado"] == "Pendiente"
    assert cita["fecha"] == manana()
    assert cita["client"]["nombre"] == "Carlos Gómez"
    assert cita["barber"]["nombre"] == "Andrés López"
    assert cita["service"]["nombre"] == "Corte Clásico"


def test_cita_en_fecha_pasada_es_rechazada(client, auth_headers, datos):
    r = client.post("/appointments/", headers=auth_headers,
                    json=cuerpo_cita(datos, fecha=ayer()))
    assert r.status_code == 400
    assert "fechas pasadas" in r.json()["detail"]


def test_cita_con_cliente_inexistente(client, auth_headers, datos):
    cuerpo = cuerpo_cita(datos)
    cuerpo["client_id"] = 999
    r = client.post("/appointments/", headers=auth_headers, json=cuerpo)
    assert r.status_code == 404
    assert r.json()["detail"] == "Cliente no encontrado"


def test_cita_con_barbero_inexistente(client, auth_headers, datos):
    cuerpo = cuerpo_cita(datos)
    cuerpo["barber_id"] = 999
    r = client.post("/appointments/", headers=auth_headers, json=cuerpo)
    assert r.status_code == 404
    assert r.json()["detail"] == "Barbero no encontrado"


def test_cita_con_servicio_inexistente(client, auth_headers, datos):
    cuerpo = cuerpo_cita(datos)
    cuerpo["service_id"] = 999
    r = client.post("/appointments/", headers=auth_headers, json=cuerpo)
    assert r.status_code == 404
    assert r.json()["detail"] == "Servicio no encontrado"


def test_cualquier_barbero_puede_atender_el_servicio(client, auth_headers, datos):
    """Los servicios son de la barbería: no están atados a un barbero."""
    cuerpo = cuerpo_cita(datos)
    cuerpo["barber_id"] = datos["otro_barbero_id"]
    r = client.post("/appointments/", headers=auth_headers, json=cuerpo)
    assert r.status_code == 200
    assert r.json()["barber"]["id"] == datos["otro_barbero_id"]


def test_horario_ocupado_es_rechazado(client, auth_headers, datos):
    client.post("/appointments/", headers=auth_headers, json=cuerpo_cita(datos))
    r = client.post("/appointments/", headers=auth_headers, json=cuerpo_cita(datos))
    assert r.status_code == 400
    assert "ya tiene una cita" in r.json()["detail"]


def test_cita_con_formato_de_fecha_invalido(client, auth_headers, datos):
    cuerpo = cuerpo_cita(datos)
    cuerpo["fecha"] = "mañana"
    r = client.post("/appointments/", headers=auth_headers, json=cuerpo)
    assert r.status_code == 422


def test_listar_y_consultar_citas(client, auth_headers, datos):
    h = auth_headers
    c1 = client.post("/appointments/", headers=h, json=cuerpo_cita(datos, hora="09:00")).json()
    client.post("/appointments/", headers=h, json=cuerpo_cita(datos, hora="10:00"))

    lista = client.get("/appointments/", headers=h)
    assert lista.status_code == 200
    assert len(lista.json()) == 2

    una = client.get(f"/appointments/{c1['id']}", headers=h)
    assert una.status_code == 200
    assert una.json()["id"] == c1["id"]


def test_consultar_cita_inexistente(client, auth_headers):
    assert client.get("/appointments/999", headers=auth_headers).status_code == 404


def test_actualizar_estado_de_la_cita(client, auth_headers, datos):
    h = auth_headers
    cita = client.post("/appointments/", headers=h, json=cuerpo_cita(datos)).json()

    cuerpo = cuerpo_cita(datos)
    cuerpo["estado"] = "Confirmada"
    r = client.put(f"/appointments/{cita['id']}", headers=h, json=cuerpo)
    assert r.status_code == 200
    assert r.json()["estado"] == "Confirmada"

    cuerpo["estado"] = "Completada"
    r = client.put(f"/appointments/{cita['id']}", headers=h, json=cuerpo)
    assert r.json()["estado"] == "Completada"


def test_estado_no_permitido_es_rechazado(client, auth_headers, datos):
    h = auth_headers
    cita = client.post("/appointments/", headers=h, json=cuerpo_cita(datos)).json()
    cuerpo = cuerpo_cita(datos)
    cuerpo["estado"] = "Finalizada"  # no existe en el enum del backend
    r = client.put(f"/appointments/{cita['id']}", headers=h, json=cuerpo)
    assert r.status_code == 422


def test_reprogramar_a_horario_ocupado_es_rechazado(client, auth_headers, datos):
    h = auth_headers
    client.post("/appointments/", headers=h, json=cuerpo_cita(datos, hora="09:00"))
    segunda = client.post("/appointments/", headers=h,
                          json=cuerpo_cita(datos, hora="10:00")).json()

    cuerpo = cuerpo_cita(datos, hora="09:00")
    cuerpo["estado"] = "Pendiente"
    r = client.put(f"/appointments/{segunda['id']}", headers=h, json=cuerpo)
    assert r.status_code == 400


def test_reprogramar_la_misma_cita_no_choca_consigo_misma(client, auth_headers, datos):
    h = auth_headers
    cita = client.post("/appointments/", headers=h, json=cuerpo_cita(datos)).json()
    cuerpo = cuerpo_cita(datos)
    cuerpo["estado"] = "Confirmada"
    assert client.put(f"/appointments/{cita['id']}", headers=h, json=cuerpo).status_code == 200


def test_actualizar_cita_a_fecha_pasada(client, auth_headers, datos):
    h = auth_headers
    cita = client.post("/appointments/", headers=h, json=cuerpo_cita(datos)).json()
    cuerpo = cuerpo_cita(datos, fecha=ayer())
    cuerpo["estado"] = "Pendiente"
    r = client.put(f"/appointments/{cita['id']}", headers=h, json=cuerpo)
    assert r.status_code == 400


def test_eliminar_cita(client, auth_headers, datos):
    h = auth_headers
    cita = client.post("/appointments/", headers=h, json=cuerpo_cita(datos)).json()
    assert client.delete(f"/appointments/{cita['id']}", headers=h).status_code == 200
    assert client.get(f"/appointments/{cita['id']}", headers=h).status_code == 404


def test_eliminar_cita_inexistente(client, auth_headers):
    assert client.delete("/appointments/999", headers=auth_headers).status_code == 404


def test_horario_liberado_tras_eliminar_la_cita(client, auth_headers, datos):
    h = auth_headers
    cita = client.post("/appointments/", headers=h, json=cuerpo_cita(datos)).json()
    client.delete(f"/appointments/{cita['id']}", headers=h)
    r = client.post("/appointments/", headers=h, json=cuerpo_cita(datos))
    assert r.status_code == 200


def test_flujo_completo_del_negocio(client, auth_headers, datos):
    """Agendar -> confirmar -> completar, y verificar el dato final."""
    h = auth_headers
    cita = client.post("/appointments/", headers=h, json=cuerpo_cita(datos)).json()
    for estado in ("Confirmada", "Completada"):
        cuerpo = cuerpo_cita(datos)
        cuerpo["estado"] = estado
        assert client.put(f"/appointments/{cita['id']}", headers=h, json=cuerpo).status_code == 200

    final = client.get(f"/appointments/{cita['id']}", headers=h).json()
    assert final["estado"] == "Completada"
    assert final["service"]["precio"] == 25000


# ---------------------------------------------------------------
# Hallazgo H-01: las citas canceladas liberan el horario
# ---------------------------------------------------------------
def _cancelar(client, h, datos, cita_id, hora="09:00"):
    """Cambia el estado de una cita a Cancelada mediante la API."""
    cuerpo = cuerpo_cita(datos, hora=hora)
    cuerpo["estado"] = "Cancelada"
    return client.put(f"/appointments/{cita_id}", headers=h, json=cuerpo)


def test_cita_cancelada_libera_el_horario(client, auth_headers, datos):
    h = auth_headers
    cita = client.post("/appointments/", headers=h, json=cuerpo_cita(datos)).json()
    assert _cancelar(client, h, datos, cita["id"]).status_code == 200
    r = client.post("/appointments/", headers=h, json=cuerpo_cita(datos))
    assert r.status_code == 200


def test_no_se_reactiva_cancelada_si_el_horario_fue_tomado(client, auth_headers, datos):
    h = auth_headers
    cancelada = client.post("/appointments/", headers=h, json=cuerpo_cita(datos)).json()
    _cancelar(client, h, datos, cancelada["id"])

    # Otro cliente toma el horario que quedó libre
    otro_cliente = client.post(
        "/clients/",
        headers=h,
        json={
            "nombre": "Luisa Pérez",
            "telefono": "3025551234",
            "email": "luisa@gmail.com",
            "barbershop_id": datos["barberia_id"],
        },
    ).json()
    cuerpo_otro = cuerpo_cita(datos)
    cuerpo_otro["client_id"] = otro_cliente["id"]
    assert client.post("/appointments/", headers=h, json=cuerpo_otro).status_code == 200

    # Intentar reactivar la cita cancelada debe rechazarse
    cuerpo = cuerpo_cita(datos)
    cuerpo["estado"] = "Pendiente"
    r = client.put(f"/appointments/{cancelada['id']}", headers=h, json=cuerpo)
    assert r.status_code == 400
    assert "ya tiene una cita" in r.json()["detail"]


# ---------------------------------------------------------------
# Citas para hoy en una hora que ya pasó
# ---------------------------------------------------------------
def _fijar_hora(monkeypatch, hora):
    """Simula que el reloj del servidor marca hoy a la hora indicada."""
    from datetime import date, datetime

    from app.services import appointment_service

    momento = datetime.combine(date.today(), hora)
    monkeypatch.setattr(appointment_service, "ahora", lambda: momento)


def test_cita_hoy_en_hora_pasada_es_rechazada(client, auth_headers, datos, monkeypatch):
    from datetime import date, time

    _fijar_hora(monkeypatch, time(22, 50))
    cuerpo = cuerpo_cita(datos, fecha=date.today().isoformat(), hora="09:00")
    r = client.post("/appointments/", headers=auth_headers, json=cuerpo)
    assert r.status_code == 400
    assert "hora que ya pasó" in r.json()["detail"]


def test_cita_de_hoy_ya_pasada_se_puede_completar(client, auth_headers, datos, monkeypatch):
    """Cambiar solo el estado no debe chocar con la validación de hora."""
    from datetime import date, time

    h = auth_headers
    hoy = date.today().isoformat()

    _fijar_hora(monkeypatch, time(8, 0))
    cita = client.post("/appointments/", headers=h,
                       json=cuerpo_cita(datos, fecha=hoy, hora="09:00")).json()

    _fijar_hora(monkeypatch, time(22, 50))
    cuerpo = cuerpo_cita(datos, fecha=hoy, hora="09:00")
    cuerpo["estado"] = "Completada"
    r = client.put(f"/appointments/{cita['id']}", headers=h, json=cuerpo)
    assert r.status_code == 200
    assert r.json()["estado"] == "Completada"

    # Pero no se puede reprogramar a otra hora que también ya pasó
    cuerpo = cuerpo_cita(datos, fecha=hoy, hora="10:00")
    cuerpo["estado"] = "Pendiente"
    r = client.put(f"/appointments/{cita['id']}", headers=h, json=cuerpo)
    assert r.status_code == 400
