from datetime import time

from pydantic import BaseModel

from app.schemas.barber_schema import BarberSimple


# ==========================================
# Crear un horario
# ==========================================
class ScheduleCreate(BaseModel):
    """
    Datos necesarios para registrar
    un horario de trabajo.
    """

    dia_semana: str
    hora_inicio: time
    hora_fin: time
    barber_id: int


# ==========================================
# Actualizar un horario
# ==========================================
class ScheduleUpdate(BaseModel):
    """
    Datos permitidos para actualizar
    un horario.
    """

    dia_semana: str
    hora_inicio: time
    hora_fin: time
    barber_id: int


# ==========================================
# Respuesta de la API
# ==========================================
class ScheduleResponse(BaseModel):
    """
    Información que devolverá
    la API al cliente.
    """

    id: int
    dia_semana: str
    hora_inicio: time
    hora_fin: time

    barber: BarberSimple

    class Config:
        from_attributes = True