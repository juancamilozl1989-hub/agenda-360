from enum import Enum

from pydantic import BaseModel

from app.schemas.barbershop_schema import BarbershopSimple


# ==========================================
# Estados permitidos para un barbero
# ==========================================
class BarberStatus(str, Enum):
    """
    Estados permitidos para un barbero.
    """

    ACTIVO = "Activo"
    INACTIVO = "Inactivo"


# ==========================================
# Crear un barbero
# ==========================================
class BarberCreate(BaseModel):
    """
    Datos necesarios para registrar
    un nuevo barbero.
    """

    nombre: str
    telefono: str
    especialidad: str

    # Si no se envía, será Activo
    estado: BarberStatus = BarberStatus.ACTIVO

    barbershop_id: int


# ==========================================
# Actualizar un barbero
# ==========================================
class BarberUpdate(BaseModel):
    """
    Datos permitidos para actualizar
    un barbero.
    """

    nombre: str
    telefono: str
    especialidad: str
    estado: BarberStatus
    barbershop_id: int


# ==========================================
# Información resumida del barbero
# ==========================================
class BarberSimple(BaseModel):
    """
    Información mínima de un barbero.
    """

    id: int
    nombre: str

    class Config:
        from_attributes = True


# ==========================================
# Respuesta de la API
# ==========================================
class BarberResponse(BaseModel):
    """
    Información que devolverá
    la API al cliente.
    """

    id: int
    nombre: str
    telefono: str
    especialidad: str
    estado: BarberStatus

    barbershop: BarbershopSimple

    class Config:
        from_attributes = True