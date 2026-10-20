"""Pruebas de integración de los horarios de los barberos."""
import pytest

pytestmark = pytest.mark.integration


def _horario(barber_id, **cambios):
    base = {"dia_semana": "Lunes", "hora_inicio": "08:00",
            "hora_fin": "17:00", "barber_id": barber_id}
    base.update(cambios)
    return base


def _barbero_sin_horario(client, h, datos):
    """Barbero nuevo, sin ningún horario registrado."""
    return client.post(
        "/barbers/", headers=h,
        json={"nombre": "Juan Rojas", "telefono": "300", "especialidad": "Color",
              "barbershop_id": datos["barberia_id"]},
    ).json()["id"]


def test_horario_crud_completo(client, auth_headers, datos):
    h = auth_headers
    bid = _barbero_sin_horario(client, h, datos)
    antes = len(client.get("/schedules/", headers=h).json())

    r = client.post("/schedules/", headers=h, json=_horario(bid))
    assert r.status_code == 200
    assert r.json()["dia_semana"] == "Lunes"
    hid = r.json()["id"]

    assert len(client.get("/schedules/", headers=h).json()) == antes + 1
    assert client.get(f"/schedules/{hid}", headers=h).status_code == 200

    actualizado = client.put(
        f"/schedules/{hid}", headers=h,
        json=_horario(bid, hora_fin="18:00"),
    )
    assert actualizado.json()["hora_fin"].startswith("18:00")

    assert client.delete(f"/schedules/{hid}", headers=h).status_code == 200
    assert client.get(f"/schedules/{hid}", headers=h).status_code == 404


def test_horario_de_barbero_inexistente(client, auth_headers):
    r = client.post("/schedules/", headers=auth_headers, json=_horario(999))
    assert r.status_code == 404


def test_el_dia_se_normaliza(client, auth_headers, datos):
    h = auth_headers
    bid = _barbero_sin_horario(client, h, datos)
    r = client.post("/schedules/", headers=h, json=_horario(bid, dia_semana="miercoles"))
    assert r.status_code == 200
    assert r.json()["dia_semana"] == "Miércoles"


def test_dia_invalido_es_rechazado(client, auth_headers, datos):
    h = auth_headers
    bid = _barbero_sin_horario(client, h, datos)
    r = client.post("/schedules/", headers=h, json=_horario(bid, dia_semana="Feriado"))
    assert r.status_code == 400
    assert "Día no válido" in r.json()["detail"]


def test_hora_fin_antes_del_inicio_es_rechazada(client, auth_headers, datos):
    h = auth_headers
    bid = _barbero_sin_horario(client, h, datos)
    r = client.post("/schedules/", headers=h,
                    json=_horario(bid, hora_inicio="17:00", hora_fin="08:00"))
    assert r.status_code == 400


def test_bloques_que_se_cruzan_son_rechazados(client, auth_headers, datos):
    h = auth_headers
    bid = _barbero_sin_horario(client, h, datos)
    client.post("/schedules/", headers=h, json=_horario(bid, hora_inicio="08:00", hora_fin="12:00"))

    cruzado = client.post("/schedules/", headers=h,
                          json=_horario(bid, hora_inicio="11:00", hora_fin="15:00"))
    assert cruzado.status_code == 400

    # Mañana y tarde sí se permiten si no se cruzan
    tarde = client.post("/schedules/", headers=h,
                        json=_horario(bid, hora_inicio="14:00", hora_fin="18:00"))
    assert tarde.status_code == 200
