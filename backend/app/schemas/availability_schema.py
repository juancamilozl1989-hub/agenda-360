from datetime import date, time

from pydantic import BaseModel, ConfigDict

from app.schemas.barber_schema import BarberSimple


# ==========================================
# Servicio consultado (datos mínimos)
# ==========================================
class ServicioConsultado(BaseModel):
    """
    Servicio para el que se calcula la disponibilidad.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    duracion: int
    precio: float


# ==========================================
# Una hora disponible
# ==========================================
class HoraDisponible(BaseModel):
    """
    Hora en la que se puede agendar y barberos libres a esa hora.
    """

    model_config = ConfigDict(from_attributes=True)

    hora: time
    barberos: list[BarberSimple]


# ==========================================
# Respuesta de la API
# ==========================================
class AvailabilityResponse(BaseModel):
    """
    Horas disponibles para un servicio en una fecha.
    """

    model_config = ConfigDict(from_attributes=True)

    fecha: date
    dia_semana: str
    servicio: ServicioConsultado
    disponibles: list[HoraDisponible]
