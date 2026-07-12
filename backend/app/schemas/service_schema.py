from pydantic import BaseModel

from app.schemas.barber_schema import BarberSimple


# ==========================================
# Crear un servicio
# ==========================================
class ServiceCreate(BaseModel):
    """
    Datos necesarios para registrar
    un nuevo servicio.
    """

    nombre: str
    descripcion: str
    precio: float
    duracion: int
    barber_id: int


# ==========================================
# Actualizar un servicio
# ==========================================
class ServiceUpdate(BaseModel):
    """
    Datos permitidos para actualizar
    un servicio.
    """

    nombre: str
    descripcion: str
    precio: float
    duracion: int
    barber_id: int


# ==========================================
# Respuesta de la API
# ==========================================
class ServiceResponse(BaseModel):
    """
    Información que devolverá
    la API al cliente.
    """

    id: int
    nombre: str
    descripcion: str
    precio: float
    duracion: int

    barber: BarberSimple

    class Config:
        from_attributes = True