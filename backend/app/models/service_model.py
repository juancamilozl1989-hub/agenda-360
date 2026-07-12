# Tipos de datos SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey

# Relaciones ORM
from sqlalchemy.orm import relationship

# Clase base
from app.core.base import Base


class Service(Base):
    """
    Modelo de los servicios que ofrece un barbero.
    """

    __tablename__ = "services"

    # Llave primaria
    id = Column(Integer, primary_key=True, index=True)

    # Nombre del servicio
    nombre = Column(String(100), nullable=False)

    # Descripción
    descripcion = Column(String(255), nullable=False)

    # Precio
    precio = Column(Float, nullable=False)

    # Duración en minutos
    duracion = Column(Integer, nullable=False)

    # Relación con el barbero
    barber_id = Column(
        Integer,
        ForeignKey("barbers.id"),
        nullable=False
    )

    # Relación ORM
    barber = relationship(
        "Barber",
        back_populates="services"
    )