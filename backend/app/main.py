import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.base import Base
from app.core.database import engine
from app.core.migraciones import (
    migrar_servicios_a_barberia,
    sincronizar_columnas,
)
from app.api.user_api import router as user_router
from app.api.barbershop_api import router as barbershop_router
from app.api.barber_api import router as barber_router
from app.api.service_api import router as service_router
from app.api.schedule_api import router as schedule_router
from app.api.client_api import router as client_router
from app.api.appointment_api import router as appointment_router
from app.api.availability_api import router as availability_router
from app.api.whatsapp_api import router as whatsapp_router

from app.core.security import (
    obtener_password_hash,
    verificar_password,
    verificar_token
)

# Importamos el modelo para que SQLAlchemy lo registre
from app.models.user_model import User
from app.models.barbershop_model import Barbershop
from app.models.barber_model import Barber
from app.models.service_model import Service
from app.models.schedule_model import Schedule
from app.models.client_model import Client
from app.models.appointment_model import Appointment
from app.models.conversation_model import Conversation

# ==========================================================
# Ciclo de vida de la aplicación
# ==========================================================
# Las tablas se crean al arrancar el servidor (no al importar el
# módulo). Así la aplicación puede importarse en las pruebas
# automatizadas sin necesidad de tener PostgreSQL encendido.
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    # Agrega columnas nuevas de los modelos a tablas que ya existían
    sincronizar_columnas(engine)
    # Los servicios pasan de pertenecer a un barbero a la barbería
    migrar_servicios_a_barberia(engine)
    yield


app = FastAPI(lifespan=lifespan)

logger = logging.getLogger("agenda360")


# ==========================================================
# Errores internos legibles
# ==========================================================
# Si ocurre un error no controlado (por ejemplo, una columna que
# no existe en la base de datos), FastAPI responde 500 SIN las
# cabeceras CORS y el navegador lo reporta como "no se pudo
# conectar con el servidor". Este middleware captura el error,
# lo deja en la consola de uvicorn y devuelve un JSON con el
# detalle. Se registra ANTES que CORS para que CORS lo envuelva
# y la respuesta sí llegue al panel.
@app.middleware("http")
async def capturar_errores(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as error:
        logger.exception("Error no controlado en %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content={
                "detail": f"Error interno del servidor: {type(error).__name__}: {error}"
            },
        )


# ==========================================================
# CORS
# ==========================================================
# Permite que el frontend (que corre en otro puerto durante
# el desarrollo) pueda comunicarse con esta API sin ser
# bloqueado por el navegador. Se acepta cualquier puerto de
# localhost, porque Vite usa 5174, 5175... si el 5173 está ocupado.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas de usuarios
app.include_router(user_router)
app.include_router(barbershop_router)
app.include_router(barber_router)
app.include_router(service_router)
app.include_router(schedule_router)
app.include_router(client_router)
app.include_router(appointment_router)
app.include_router(availability_router)
app.include_router(whatsapp_router)

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