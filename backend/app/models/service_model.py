# Tipos de datos SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey

# Relaciones ORM
from sqlalchemy.orm import relationship

# Clase base
from app.core.base import Base


class Service(Base):
    """
    Modelo de los servicios que ofrece la barbería.

    Los servicios forman el catálogo de la barbería: cualquier
    barbero activo puede atender cualquier servicio activo.
    """

    __tablename__ = "services"

    # Llave primaria
    id = Column(Integer, primary_key=True, index=True)

    # Nombre del servicio
    nombre = Column(String(100), nullable=False)

    # Categoría
    categoria = Column(
        String(50),
        nullable=False
    )

    # Descripción
    descripcion = Column(
        String(255),
        nullable=False
    )

    # Precio
    precio = Column(
        Float,
        nullable=False
    )

    # Duración en minutos
    duracion = Column(
        Integer,
        nullable=False
    )

    # Estado
    estado = Column(
        String(20),
        nullable=False,
        default="Activo"
    )

    # Relación con la barbería
    barbershop_id = Column(
        Integer,
        ForeignKey("barbershops.id"),
        nullable=False
    )

    # Relación ORM
    barbershop = relationship(
        "Barbershop",
        back_populates="services"
    )

    # Citas asociadas al servicio
    appointments = relationship(
        "Appointment",
        back_populates="service",
        cascade="all, delete-orphan"
    )