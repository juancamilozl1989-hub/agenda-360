from enum import Enum

from pydantic import BaseModel, EmailStr


# ==========================================
# Estados permitidos para una barbería
# ==========================================
class BarbershopStatus(str, Enum):
    """
    Estados permitidos para una barbería.
    """

    ACTIVA = "Activa"
    INACTIVA = "Inactiva"


# ==========================================
# Crear una barbería
# ==========================================
class BarbershopCreate(BaseModel):
    """
    Datos necesarios para registrar
    una barbería.
    """

    nombre: str
    direccion: str
    telefono: str
    email: EmailStr


# ==========================================
# Actualizar una barbería
# ==========================================
class BarbershopUpdate(BaseModel):
    """
    Datos para actualizar una barbería.
    """

    nombre: str
    direccion: str
    telefono: str
    email: EmailStr
    estado: BarbershopStatus


# ==========================================
# Respuesta de la API
# ==========================================
class BarbershopResponse(BaseModel):
    """
    Información que devolverá la API.
    """

    id: int
    nombre: str
    direccion: str
    telefono: str
    email: str
    estado: BarbershopStatus

    class Config:
        from_attributes = True


# ==========================================
# Información básica de una barbería
# ==========================================
class BarbershopSimple(BaseModel):
    """
    Información mínima de una barbería.

    Este esquema será utilizado cuando
    otros módulos necesiten mostrar
    únicamente los datos básicos de
    la barbería.
    """

    id: int
    nombre: str

    class Config:
        from_attributes = True