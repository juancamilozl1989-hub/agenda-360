"""Pruebas de integración de la gestión de usuarios y validaciones extra de servicios."""
import pytest

pytestmark = pytest.mark.integration


def test_listar_y_consultar_usuarios(client, auth_headers):
    lista = client.get("/users/", headers=auth_headers)
    assert lista.status_code == 200
    assert lista.json()[0]["email"] == "admin@agenda360.com"
    # La respuesta nunca debe incluir la contraseña
    assert "password" not in lista.json()[0]

    uid = lista.json()[0]["id"]
    una = client.get(f"/users/{uid}", headers=auth_headers)
    assert una.status_code == 200
    assert una.json()["nombre"] == "Admin Pruebas"


def test_usuario_inexistente(client, auth_headers):
    assert client.get("/users/999", headers=auth_headers).status_code == 404
    assert client.delete("/users/999", headers=auth_headers).status_code == 404
    r = client.put("/users/999", headers=auth_headers,
                   json={"nombre": "X", "email": "x@x.com"})
    assert r.status_code == 404


def test_actualizar_usuario(client, auth_headers):
    uid = client.get("/users/", headers=auth_headers).json()[0]["id"]
    r = client.put(f"/users/{uid}", headers=auth_headers,
                   json={"nombre": "Nuevo Nombre", "email": "nuevo@agenda360.com"})
    assert r.status_code == 200
    assert r.json()["nombre"] == "Nuevo Nombre"


def test_actualizar_usuario_con_correo_invalido(client, auth_headers):
    uid = client.get("/users/", headers=auth_headers).json()[0]["id"]
    r = client.put(f"/users/{uid}", headers=auth_headers,
                   json={"nombre": "X", "email": "no-es-correo"})
    assert r.status_code == 422


def test_eliminar_usuario(client, auth_headers):
    uid = client.get("/users/", headers=auth_headers).json()[0]["id"]
    assert client.delete(f"/users/{uid}", headers=auth_headers).status_code == 200


def test_actualizar_servicio_con_datos_invalidos(client, auth_headers, datos):
    h = auth_headers
    cuerpo = {"nombre": "X", "categoria": "Corte", "descripcion": "x",
              "precio": 100, "duracion": 10, "estado": "Activo",
              "barbershop_id": datos["barberia_id"]}

    assert client.put("/services/999", headers=h, json=cuerpo).status_code == 404
    assert client.put(f"/services/{datos['servicio_id']}", headers=h,
                      json={**cuerpo, "precio": 0}).status_code == 400
    assert client.put(f"/services/{datos['servicio_id']}", headers=h,
                      json={**cuerpo, "duracion": 0}).status_code == 400
    assert client.put(f"/services/{datos['servicio_id']}", headers=h,
                      json={**cuerpo, "estado": "Raro"}).status_code == 400
    assert client.put(f"/services/{datos['servicio_id']}", headers=h,
                      json={**cuerpo, "barbershop_id": 999}).status_code == 404
