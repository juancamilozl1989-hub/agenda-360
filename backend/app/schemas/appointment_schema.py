from datetime import date, time

from pydantic import BaseModel

from app.schemas.client_schema import ClientResponse
from app.schemas.barber_schema import BarberSimple
from app.schemas.service_schema import ServiceResponse


# ==========================================
# Crear una cita
# ==========================================
class AppointmentCreate(BaseModel):
    """
    Datos necesarios para registrar
    una nueva cita.
    """

    fecha: date
    hora: time
    client_id: int
    barber_id: int
    service_id: int


# ==========================================
# Actualizar una cita
# ==========================================
class AppointmentUpdate(BaseModel):
    """
    Datos permitidos para actualizar
    una cita.
    """

    fecha: date
    hora: time
    estado: str
    client_id: int
    barber_id: int
    service_id: int


# ==========================================
# Respuesta de la API
# ==========================================
class AppointmentResponse(BaseModel):
    """
    Información que devolverá
    la API al cliente.
    """

    id: int
    fecha: date
    hora: time
    estado: str

    client: ClientResponse
    barber: BarberSimple
    service: ServiceResponse

    class Config:
        from_attributes = True