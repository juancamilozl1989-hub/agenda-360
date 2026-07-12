# Tipos de datos SQL
from sqlalchemy import Column, Integer, String, ForeignKey

# Permite crear relaciones entre modelos
from sqlalchemy.orm import relationship

# Clase base
from app.core.base import Base


class Barber(Base):
    """
    Modelo de los barberos.
    """

    __tablename__ = "barbers"

    # Llave primaria
    id = Column(Integer, primary_key=True, index=True)

    # Nombre del barbero
    nombre = Column(String(100), nullable=False)

    # Teléfono
    telefono = Column(String(20), nullable=False)

    # Relación con la barbería
    barbershop_id = Column(
        Integer,
        ForeignKey("barbershops.id"),
        nullable=False
    )

    # Relación ORM
    barbershop = relationship(
        "Barbershop",
        back_populates="barbers"
    )

    # Servicios del barbero
    services = relationship(
        "Service",
        back_populates="barber",
        cascade="all, delete-orphan"
    )
    
