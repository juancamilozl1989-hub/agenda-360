# Tipos de datos SQLAlchemy
from sqlalchemy import Column, Integer, String, Time, ForeignKey

# Relaciones ORM
from sqlalchemy.orm import relationship

# Clase base
from app.core.base import Base


class Schedule(Base):
    """
    Modelo de los horarios de trabajo
    de cada barbero.
    """

    __tablename__ = "schedules"

    # Llave primaria
    id = Column(Integer, primary_key=True, index=True)

    # Día de la semana
    dia_semana = Column(String(20), nullable=False)

    # Hora de inicio
    hora_inicio = Column(Time, nullable=False)

    # Hora de finalización
    hora_fin = Column(Time, nullable=False)

    # Relación con el barbero
    barber_id = Column(
        Integer,
        ForeignKey("barbers.id"),
        nullable=False
    )

    # Relación ORM
    barber = relationship(
        "Barber",
        back_populates="schedules"
    )