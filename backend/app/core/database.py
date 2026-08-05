# Permite crear la conexión con PostgreSQL
from sqlalchemy import create_engine

# Permite crear sesiones para consultar la base de datos
from sqlalchemy.orm import sessionmaker, declarative_base

# Variables cargadas desde .env
from app.core.config import (
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_NAME,
    DATABASE_USER,
    DATABASE_PASSWORD,
)

# Construcción de la URL de conexión
DATABASE_URL = (
    f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}"
    f"@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

# Conexión principal
engine = create_engine(DATABASE_URL)

# Sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Clase base para todos los modelos
Base = declarative_base()


# Dependencia para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()