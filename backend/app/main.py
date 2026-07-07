from fastapi import FastAPI
from app.core.base import Base
from app.core.database import engine
from app.api.user_api import router as user_router
from app.api.barbershop_api import router as barbershop_router
from app.api.barber_api import router as barber_router

from app.core.security import (
    obtener_password_hash,
    verificar_password,
    verificar_token
)

# Importamos el modelo para que SQLAlchemy lo registre
from app.models.user_model import User
from app.models.barbershop_model import Barbershop
from app.models.barber_model import Barber

app = FastAPI()

# Registrar rutas de usuarios
app.include_router(user_router)
app.include_router(barbershop_router)
app.include_router(barber_router)

# Crear tablas automáticamente
Base.metadata.create_all(bind=engine)

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a Agenda 360"}


@app.get("/test-db")
def test_db():
    try:
        connection = engine.connect()
        connection.close()

        return {
            "estado": "ok",
            "mensaje": "Conexión exitosa con PostgreSQL"
        }

    except Exception as e:
        return {
            "estado": "error",
            "detalle": str(e)
        }
        
# ==========================================================
# Prueba temporal de seguridad
# ==========================================================
@app.get("/test-security")
def test_security():
    """
    Endpoint temporal para comprobar
    el funcionamiento de bcrypt.
    """

    password = "123456"

    # Generar hash
    password_hash = obtener_password_hash(password)

    # Verificar contraseña
    es_valida = verificar_password(
        password,
        password_hash
    )

    return {
        "password_original": password,
        "password_hash": password_hash,
        "password_valida": es_valida
    }
    
from fastapi import Header

@app.get("/verify-token")
def verify_token_endpoint(
    authorization: str = Header(...)
):
    """
    Verifica un JWT enviado en el encabezado Authorization.
    """

    # El encabezado llega así:
    # Bearer eyJhbGciOi...

    token = authorization.replace("Bearer ", "")

    payload = verificar_token(token)

    return {
        "mensaje": "Token válido",
        "datos": payload
    }
    
