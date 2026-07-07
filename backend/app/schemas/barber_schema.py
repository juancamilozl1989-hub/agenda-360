from pydantic import BaseModel


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
    barbershop_id: int

    class Config:
        from_attributes = True