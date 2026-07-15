# Tipos de datos SQL
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Clase base común
from app.core.base import Base


class Barbershop(Base):
    """
    Modelo de barberías.

    Cada registro representa una barbería
    registrada dentro del sistema.
    """

    __tablename__ = "barbershops"

    # Llave primaria
    id = Column(Integer, primary_key=True, index=True)

    # Nombre de la barbería
    nombre = Column(String(100), nullable=False)

    # Dirección
    direccion = Column(String(200), nullable=False)

    # Teléfono
    telefono = Column(String(20), nullable=False)

    # Correo electrónico
    email = Column(String(150), nullable=False)
    
    # Lista de barberos que pertenecen a esta barbería
    barbers = relationship(
        "Barber",
        back_populates="barbershop",
        cascade="all, delete-orphan"
)

    # Lista de clientes que pertenecen a esta barbería
    clients = relationship(
        "Client",
        back_populates="barbershop",
        cascade="all, delete-orphan"
)