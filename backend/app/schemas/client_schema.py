from pydantic import BaseModel

from app.schemas.barbershop_schema import BarbershopSimple


# ==========================================
# Crear un cliente
# ==========================================
class ClientCreate(BaseModel):
    """
    Datos necesarios para registrar
    un nuevo cliente.
    """

    nombre: str
    telefono: str
    email: str
    barbershop_id: int


# ==========================================
# Actualizar un cliente
# ==========================================
class ClientUpdate(BaseModel):
    """
    Datos permitidos para actualizar
    un cliente.
    """

    nombre: str
    telefono: str
    email: str
    barbershop_id: int


# ==========================================
# Respuesta de la API
# ==========================================
class ClientResponse(BaseModel):
    """
    Información que devolverá
    la API al cliente.
    """

    id: int
    nombre: str
    telefono: str
    email: str

    barbershop: BarbershopSimple

    class Config:
        from_attributes = True