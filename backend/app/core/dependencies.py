# Permite abrir y cerrar sesiones con PostgreSQL

from app.core.database import SessionLocal


def get_db():
    """
    Abre una sesión de base de datos
    y la cierra automáticamente al terminar.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()