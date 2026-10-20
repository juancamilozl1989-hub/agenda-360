"""Pruebas de integración de autenticación (registro, login y rutas protegidas)."""
import pytest

pytestmark = pytest.mark.integration

USUARIO = {"nombre": "Admin", "email": "admin@agenda360.com", "password": "Clave12345"}


def test_registro_de_usuario(client):
    r = client.post("/users/", json=USUARIO)
    assert r.status_code == 200
    assert r.json()["mensaje"] == "Usuario creado correctamente"


def test_registro_con_correo_repetido_no_duplica(client):
    client.post("/users/", json=USUARIO)
    r = client.post("/users/", json=USUARIO)
    assert r.json()["mensaje"] == "El correo ya se encuentra registrado"


def test_login_correcto_devuelve_token(client):
    client.post("/users/", json=USUARIO)
    r = client.post(
        "/users/login",
        data={"username": USUARIO["email"], "password": USUARIO["password"]},
    )
    assert r.status_code == 200
    assert r.json()["token_type"] == "bearer"
    assert r.json()["access_token"]


def test_login_con_clave_incorrecta(client):
    client.post("/users/", json=USUARIO)
    r = client.post(
        "/users/login",
        data={"username": USUARIO["email"], "password": "incorrecta"},
    )
    assert r.status_code == 401


def test_login_con_usuario_inexistente(client):
    r = client.post(
        "/users/login", data={"username": "nadie@x.com", "password": "123"}
    )
    assert r.status_code == 401


def test_la_contrasena_se_guarda_cifrada(client, db):
    from app.models.user_model import User

    client.post("/users/", json=USUARIO)
    usuario = db.query(User).filter(User.email == USUARIO["email"]).first()
    assert usuario.password != USUARIO["password"]


@pytest.mark.parametrize(
    "ruta",
    ["/barbershops/", "/barbers/", "/clients/", "/services/", "/schedules/",
     "/appointments/", "/users/"],
)
def test_rutas_protegidas_sin_token_responden_401(client, ruta):
    assert client.get(ruta).status_code == 401


def test_token_invalido_es_rechazado(client):
    r = client.get("/clients/", headers={"Authorization": "Bearer token-falso"})
    assert r.status_code == 401


def test_token_valido_permite_acceder(client, auth_headers):
    assert client.get("/clients/", headers=auth_headers).status_code == 200
