"""
Configuración común de las pruebas de Agenda 360.

Las pruebas NO tocan la base de datos real del proyecto: cada prueba
trabaja sobre una base limpia que se crea y se destruye automáticamente.

Por defecto se usa SQLite en memoria, de modo que las pruebas corren en
cualquier equipo sin instalar nada. Si se quiere probar contra PostgreSQL
(el motor real del proyecto) basta con definir la variable de entorno:

    TEST_DATABASE_URL=postgresql://usuario:clave@localhost:5432/agenda360_test
"""
import os
from datetime import date, timedelta

# Estas variables deben existir ANTES de importar la aplicación, porque
# app.core.config las lee al cargarse. Valores ficticios, solo para pruebas.
os.environ.setdefault("SECRET_KEY", "clave-solo-para-pruebas")
os.environ.setdefault("DATABASE_HOST", "localhost")
os.environ.setdefault("DATABASE_PORT", "5432")
os.environ.setdefault("DATABASE_NAME", "agenda360_pruebas")
os.environ.setdefault("DATABASE_USER", "pruebas")
os.environ.setdefault("DATABASE_PASSWORD", "pruebas")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.base import Base
from app.core.dependencies import get_db
from app.main import app
from app.utils.agenda import DIAS_SEMANA

# Se importan todos los modelos para que Base conozca todas las tablas
from app.models import (  # noqa: F401
    appointment_model,
    barber_model,
    barbershop_model,
    client_model,
    schedule_model,
    service_model,
    user_model,
)

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite://")


@pytest.fixture()
def engine():
    """Motor de base de datos limpio para cada prueba."""
    if TEST_DATABASE_URL.startswith("sqlite"):
        motor = create_engine(
            TEST_DATABASE_URL,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    else:
        motor = create_engine(TEST_DATABASE_URL)

    Base.metadata.drop_all(bind=motor)
    Base.metadata.create_all(bind=motor)
    yield motor
    Base.metadata.drop_all(bind=motor)
    motor.dispose()


@pytest.fixture()
def db(engine):
    """Sesión de base de datos para pruebas unitarias directas."""
    Sesion = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    sesion = Sesion()
    try:
        yield sesion
    finally:
        sesion.close()


@pytest.fixture()
def client(engine):
    """Cliente HTTP de pruebas con la base de datos de prueba conectada."""
    Sesion = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    def _get_db_prueba():
        sesion = Sesion()
        try:
            yield sesion
        finally:
            sesion.close()

    app.dependency_overrides[get_db] = _get_db_prueba
    # Sin "with": así no se ejecuta el evento de arranque, que intentaría
    # crear las tablas en la base de datos real del proyecto.
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def auth_headers(client):
    """Registra un usuario, inicia sesión y devuelve el encabezado JWT."""
    client.post(
        "/users/",
        json={
            "nombre": "Admin Pruebas",
            "email": "admin@agenda360.com",
            "password": "Clave12345",
        },
    )
    respuesta = client.post(
        "/users/login",
        data={"username": "admin@agenda360.com", "password": "Clave12345"},
    )
    token = respuesta.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------
# Datos de apoyo: crean registros a través de la API
# ---------------------------------------------------------------
@pytest.fixture()
def datos(client, auth_headers):
    """
    Crea una barbería con dos barberos, un servicio del catálogo
    de la barbería y un cliente. Ambos barberos atienden todos los
    días de 08:00 a 20:00, para que las reglas de horario no
    interfieran en las pruebas que no tratan de horarios.
    Devuelve los identificadores.
    """
    h = auth_headers
    barberia = client.post(
        "/barbershops/",
        headers=h,
        json={
            "nombre": "Barbería Central",
            "direccion": "Calle 10 # 20-30",
            "telefono": "3001112233",
            "email": "central@agenda360.com",
        },
    ).json()

    barbero = client.post(
        "/barbers/",
        headers=h,
        json={
            "nombre": "Andrés López",
            "telefono": "3001234567",
            "especialidad": "Fade",
            "barbershop_id": barberia["id"],
        },
    ).json()

    otro_barbero = client.post(
        "/barbers/",
        headers=h,
        json={
            "nombre": "Sebastián Gómez",
            "telefono": "3014567890",
            "especialidad": "Barba",
            "barbershop_id": barberia["id"],
        },
    ).json()

    servicio = client.post(
        "/services/",
        headers=h,
        json={
            "nombre": "Corte Clásico",
            "categoria": "Corte",
            "descripcion": "Corte con tijera y máquina",
            "precio": 25000,
            "duracion": 30,
            "barbershop_id": barberia["id"],
        },
    ).json()

    for barbero_id in (barbero["id"], otro_barbero["id"]):
        for dia in DIAS_SEMANA:
            client.post(
                "/schedules/",
                headers=h,
                json={
                    "dia_semana": dia,
                    "hora_inicio": "08:00",
                    "hora_fin": "20:00",
                    "barber_id": barbero_id,
                },
            )

    cliente = client.post(
        "/clients/",
        headers=h,
        json={
            "nombre": "Carlos Gómez",
            "telefono": "3019876543",
            "email": "carlos@gmail.com",
            "barbershop_id": barberia["id"],
        },
    ).json()

    return {
        "barberia_id": barberia["id"],
        "barbero_id": barbero["id"],
        "otro_barbero_id": otro_barbero["id"],
        "servicio_id": servicio["id"],
        "cliente_id": cliente["id"],
    }


def manana() -> str:
    """Fecha de mañana en formato AAAA-MM-DD."""
    return (date.today() + timedelta(days=1)).isoformat()


def ayer() -> str:
    """Fecha de ayer en formato AAAA-MM-DD."""
    return (date.today() - timedelta(days=1)).isoformat()


def cuerpo_cita(datos: dict, fecha: str | None = None, hora: str = "09:00") -> dict:
    """Arma el cuerpo JSON de una cita con los datos de apoyo."""
    return {
        "fecha": fecha or manana(),
        "hora": hora,
        "client_id": datos["cliente_id"],
        "barber_id": datos["barbero_id"],
        "service_id": datos["servicio_id"],
    }
