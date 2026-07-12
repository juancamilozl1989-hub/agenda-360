from pydantic import BaseModel
from app.schemas.barbershop_schema import BarbershopSimple


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

    barbershop: BarbershopSimple

    class Config:
        from_attributes = True