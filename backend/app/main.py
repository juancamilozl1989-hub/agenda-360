from fastapi import FastAPI
from app.core.base import Base
from app.core.database import engine
from app.api.user_api import router as user_router

# Importamos el modelo para que SQLAlchemy lo registre
from app.models.user_model import User

app = FastAPI()

# Registrar rutas de usuarios
app.include_router(user_router)

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