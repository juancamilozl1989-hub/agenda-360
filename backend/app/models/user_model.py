# Tipos de datos SQL
from sqlalchemy import Column, Integer, String

# Clase base común de la aplicación
from app.core.base import Base


class User(Base):
    """
    Modelo de usuarios del sistema.

    Esta clase se convertirá automáticamente
    en una tabla dentro de PostgreSQL.
    """

    # Nombre de la tabla
    __tablename__ = "users"

    # Llave primaria
    id = Column(Integer, primary_key=True, index=True)

    # Nombre completo del usuario
    nombre = Column(String(100), nullable=False)

    # Correo electrónico
    email = Column(String(150), unique=True, nullable=False)

    # Contraseña
    password = Column(String(255), nullable=False)