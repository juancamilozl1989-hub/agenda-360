"""Pruebas de integración del CRUD de barberías, barberos, clientes y servicios."""
import pytest

pytestmark = pytest.mark.integration


# ---------------------------- Barberías ----------------------------
def test_barberia_crud_completo(client, auth_headers):
    h = auth_headers
    creada = client.post(
        "/barbershops/",
        headers=h,
        json={"nombre": "Central", "direccion": "Cll 1", "telefono": "300",
              "email": "central@agenda360.com"},
    )
    assert creada.status_code == 200
    assert creada.json()["estado"] == "Activa"
    bid = creada.json()["id"]

    assert client.get(f"/barbershops/{bid}", headers=h).json()["nombre"] == "Central"

    actualizada = client.put(
        f"/barbershops/{bid}",
        headers=h,
        json={"nombre": "Central Plus", "direccion": "Cll 2", "telefono": "301",
              "email": "plus@agenda360.com", "estado": "Inactiva"},
    )
    assert actualizada.json()["nombre"] == "Central Plus"
    assert actualizada.json()["estado"] == "Inactiva"

    assert client.delete(f"/barbershops/{bid}", headers=h).status_code == 200
    assert client.get(f"/barbershops/{bid}", headers=h).status_code == 404


def test_barberia_con_correo_invalido_es_rechazada(client, auth_headers):
    r = client.post(
        "/barbershops/",
        headers=auth_headers,
        json={"nombre": "X", "direccion": "Y", "telefono": "1", "email": "no-es-correo"},
    )
    assert r.status_code == 422


# ----------------------------- Barberos -----------------------------
def test_barbero_crud_completo(client, auth_headers, datos):
    h = auth_headers
    r = client.post(
        "/barbers/",
        headers=h,
        json={"nombre": "Juan Rojas", "telefono": "3209876543",
              "especialidad": "Color", "barbershop_id": datos["barberia_id"]},
    )
    assert r.status_code == 200
    assert r.json()["estado"] == "Activo"
    assert r.json()["barbershop"]["id"] == datos["barberia_id"]
    bid = r.json()["id"]

    actualizado = client.put(
        f"/barbers/{bid}",
        headers=h,
        json={"nombre": "Juan Rojas", "telefono": "3209876543",
              "especialidad": "Barba", "estado": "Inactivo",
              "barbershop_id": datos["barberia_id"]},
    )
    assert actualizado.json()["especialidad"] == "Barba"
    assert actualizado.json()["estado"] == "Inactivo"

    assert client.delete(f"/barbers/{bid}", headers=h).status_code == 200
    assert client.get(f"/barbers/{bid}", headers=h).status_code == 404


def test_barbero_en_barberia_inexistente(client, auth_headers):
    r = client.post(
        "/barbers/",
        headers=auth_headers,
        json={"nombre": "X", "telefono": "1", "especialidad": "Y", "barbershop_id": 999},
    )
    assert r.status_code == 404


def test_listar_barberos(client, auth_headers, datos):
    r = client.get("/barbers/", headers=auth_headers)
    assert r.status_code == 200
    assert len(r.json()) == 2


# ------------------------------ Clientes ------------------------------
def test_cliente_crud_completo(client, auth_headers, datos):
    h = auth_headers
    cid = datos["cliente_id"]

    leido = client.get(f"/clients/{cid}", headers=h)
    assert leido.status_code == 200
    assert leido.json()["email"] == "carlos@gmail.com"
    assert leido.json()["estado"] == "Activo"

    actualizado = client.put(
        f"/clients/{cid}",
        headers=h,
        json={"nombre": "Carlos G.", "telefono": "3000000000",
              "email": "nuevo@gmail.com", "estado": "Inactivo",
              "barbershop_id": datos["barberia_id"]},
    )
    assert actualizado.json()["nombre"] == "Carlos G."
    assert actualizado.json()["estado"] == "Inactivo"

    assert client.delete(f"/clients/{cid}", headers=h).status_code == 200
    assert client.get(f"/clients/{cid}", headers=h).status_code == 404


def test_cliente_en_barberia_inexistente(client, auth_headers):
    r = client.post(
        "/clients/",
        headers=auth_headers,
        json={"nombre": "X", "telefono": "1", "email": "x@x.com", "barbershop_id": 999},
    )
    assert r.status_code == 404


def test_cliente_sin_campos_obligatorios(client, auth_headers):
    r = client.post("/clients/", headers=auth_headers, json={"nombre": "Solo nombre"})
    assert r.status_code == 422


def test_cliente_inexistente_devuelve_404(client, auth_headers):
    assert client.get("/clients/999", headers=auth_headers).status_code == 404


# ------------------------------ Servicios ------------------------------
def _servicio(datos, **cambios):
    base = {"nombre": "Barba Premium", "categoria": "Barba",
            "descripcion": "Perfilado y toalla caliente", "precio": 18000,
            "duracion": 25, "barbershop_id": datos["barberia_id"]}
    base.update(cambios)
    return base


def test_servicio_crud_completo(client, auth_headers, datos):
    h = auth_headers
    r = client.post("/services/", headers=h, json=_servicio(datos))
    assert r.status_code == 200
    assert r.json()["estado"] == "Activo"
    assert r.json()["barbershop"]["id"] == datos["barberia_id"]
    sid = r.json()["id"]

    actualizado = client.put(
        f"/services/{sid}",
        headers=h,
        json=_servicio(datos, precio=20000, estado="Inactivo"),
    )
    assert actualizado.json()["precio"] == 20000
    assert actualizado.json()["estado"] == "Inactivo"

    assert client.delete(f"/services/{sid}", headers=h).status_code == 200
    assert client.get(f"/services/{sid}", headers=h).status_code == 404


@pytest.mark.parametrize("precio", [0, -5000])
def test_servicio_con_precio_no_positivo(client, auth_headers, datos, precio):
    r = client.post("/services/", headers=auth_headers, json=_servicio(datos, precio=precio))
    assert r.status_code == 400
    assert "precio" in r.json()["detail"]


@pytest.mark.parametrize("duracion", [0, -10])
def test_servicio_con_duracion_no_positiva(client, auth_headers, datos, duracion):
    r = client.post("/services/", headers=auth_headers, json=_servicio(datos, duracion=duracion))
    assert r.status_code == 400
    assert "duración" in r.json()["detail"]


def test_servicio_con_estado_invalido(client, auth_headers, datos):
    r = client.post("/services/", headers=auth_headers, json=_servicio(datos, estado="Raro"))
    assert r.status_code == 400


def test_servicio_de_barberia_inexistente(client, auth_headers):
    r = client.post(
        "/services/",
        headers=auth_headers,
        json={"nombre": "X", "categoria": "Corte", "descripcion": "x",
              "precio": 100, "duracion": 10, "barbershop_id": 999},
    )
    assert r.status_code == 404
    assert "Barbería" in r.json()["detail"]
