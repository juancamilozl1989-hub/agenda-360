from pydantic import BaseModel, EmailStr


class BarbershopCreate(BaseModel):
    """
    Datos necesarios para registrar una barbería.
    """

    nombre: str
    direccion: str
    telefono: str
    email: EmailStr


class BarbershopUpdate(BaseModel):
    """
    Datos para actualizar una barbería.
    """

    nombre: str
    direccion: str
    telefono: str
    email: EmailStr


class BarbershopResponse(BaseModel):
    """
    Información que devolverá la API.
    """

    id: int
    nombre: str
    direccion: str
    telefono: str
    email: str

    class Config:
        from_attributes = True