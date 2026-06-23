from fastapi import FastAPI

from app.core.database import engine

app = FastAPI()


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