# Tipos de datos SQLAlchemy
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    ForeignKey
)

# Relaciones ORM
from sqlalchemy.orm import relationship

# Clase base
from app.core.base import Base


class Appointment(Base):
    """
    Modelo de las citas.
    """

    __tablename__ = "appointments"

    # Llave primaria
    id = Column(Integer, primary_key=True, index=True)

    # Fecha de la cita
    fecha = Column(Date, nullable=False)

    # Hora de la cita
    hora = Column(Time, nullable=False)

    # Estado de la cita
    estado = Column(
        String(30),
        nullable=False,
        default="Pendiente"
    )

    # Cliente
    client_id = Column(
        Integer,
        ForeignKey("clients.id"),
        nullable=False
    )

    # Barbero
    barber_id = Column(
        Integer,
        ForeignKey("barbers.id"),
        nullable=False
    )

    # Servicio
    service_id = Column(
        Integer,
        ForeignKey("services.id"),
        nullable=False
    )

    # Relaciones ORM
    client = relationship(
        "Client",
        back_populates="appointments"
    )

    barber = relationship(
        "Barber",
        back_populates="appointments"
    )

    service = relationship(
        "Service",
        back_populates="appointments"
    )