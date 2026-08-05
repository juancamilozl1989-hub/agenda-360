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
    categoria: str
    descripcion: str
    precio: float
    duracion: int
    estado: str = "Activo"
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
    categoria: str
    descripcion: str
    precio: float
    duracion: int
    estado: str
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
    categoria: str
    descripcion: str
    precio: float
    duracion: int
    estado: str

    barber: BarberSimple

    class Config:
        from_attributes = True