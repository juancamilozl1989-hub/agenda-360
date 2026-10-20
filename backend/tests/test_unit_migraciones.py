"""
Pruebas de la sincronización del esquema (app/core/migraciones.py).

Simulan una base de datos creada con una versión anterior del sistema:
la tabla clients sin la columna "estado" (hallazgo H-11) y la tabla
services con barber_id en lugar de barbershop_id (hallazgo H-13).
Se usa siempre una base SQLite propia, independiente de la de las demás pruebas.
"""
import pytest
from sqlalchemy import create_engine, inspect, text

from app.core.base import Base
from app.core.migraciones import migrar_servicios_a_barberia, sincronizar_columnas

pytestmark = pytest.mark.unit


@pytest.fixture()
def base_antigua():
    motor = create_engine("sqlite://")
    with motor.begin() as c:
        c.execute(text("CREATE TABLE barbershops (id INTEGER PRIMARY KEY, nombre VARCHAR(100), "
                       "direccion VARCHAR(200), telefono VARCHAR(20), email VARCHAR(150), estado VARCHAR(20))"))
        c.execute(text("CREATE TABLE barbers (id INTEGER PRIMARY KEY, nombre VARCHAR(100), telefono VARCHAR(20), "
                       "especialidad VARCHAR(100), estado VARCHAR(20), barbershop_id INTEGER)"))
        c.execute(text("CREATE TABLE clients (id INTEGER PRIMARY KEY, nombre VARCHAR(100), telefono VARCHAR(20), "
                       "email VARCHAR(100), barbershop_id INTEGER)"))
        c.execute(text("CREATE TABLE services (id INTEGER PRIMARY KEY, nombre VARCHAR(100), categoria VARCHAR(50), "
                       "descripcion VARCHAR(255), precio FLOAT, duracion INTEGER, estado VARCHAR(20), barber_id INTEGER)"))
        c.execute(text("INSERT INTO barbershops VALUES (1,'Central','x','1','a@a.com','Activa'), (2,'Norte','x','1','b@b.com','Activa')"))
        c.execute(text("INSERT INTO barbers VALUES (7,'Andrés','1','Fade','Activo',2)"))
        c.execute(text("INSERT INTO clients VALUES (1,'Carlos','1','c@c.com',1)"))
        c.execute(text("INSERT INTO services VALUES (1,'Corte','Corte','x',25000,30,'Activo',7), "
                       "(2,'Barba','Barba','x',18000,20,'Activo',99)"))
    Base.metadata.create_all(bind=motor)  # crea solo las tablas que faltan
    yield motor
    motor.dispose()


def test_agrega_columnas_faltantes_con_su_valor_por_defecto(base_antigua):
    agregadas = sincronizar_columnas(base_antigua)

    assert "clients.estado" in agregadas
    assert "services.barbershop_id" in agregadas
    with base_antigua.connect() as c:
        assert c.execute(text("SELECT estado FROM clients")).scalar() == "Activo"


def test_sincronizar_dos_veces_no_repite_cambios(base_antigua):
    sincronizar_columnas(base_antigua)
    assert sincronizar_columnas(base_antigua) == []


def test_servicios_pasan_a_la_barberia_de_su_antiguo_barbero(base_antigua):
    sincronizar_columnas(base_antigua)
    assert migrar_servicios_a_barberia(base_antigua) is True

    columnas = {c["name"] for c in inspect(base_antigua).get_columns("services")}
    assert "barber_id" not in columnas

    with base_antigua.connect() as c:
        filas = dict(c.execute(text("SELECT id, barbershop_id FROM services")).fetchall())
    assert filas[1] == 2  # el barbero 7 era de la barbería 2
    assert filas[2] == 1  # barbero inexistente: se asigna la primera barbería


def test_migracion_de_servicios_solo_se_aplica_una_vez(base_antigua):
    sincronizar_columnas(base_antigua)
    migrar_servicios_a_barberia(base_antigua)
    assert migrar_servicios_a_barberia(base_antigua) is False
