# Tipos de datos SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey

# Relaciones ORM
from sqlalchemy.orm import relationship

# Clase base
from app.core.base import Base


class Client(Base):
    """
    Modelo de los clientes
    de una barbería.
    """

    __tablename__ = "clients"

    # Llave primaria
    id = Column(Integer, primary_key=True, index=True)

    # Nombre del cliente
    nombre = Column(String(100), nullable=False)

    # Teléfono
    telefono = Column(String(20), nullable=False)

    # Correo electrónico
    email = Column(String(100), nullable=False)

    # Relación con la barbería
    barbershop_id = Column(
        Integer,
        ForeignKey("barbershops.id"),
        nullable=False
    )
    
        # Relación ORM
    barbershop = relationship(
        "Barbershop",
        back_populates="clients"
    )
    
    # Citas del cliente
    appointments = relationship(
        "Appointment",
        back_populates="client",
        cascade="all, delete-orphan"
)