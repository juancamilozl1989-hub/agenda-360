from pydantic import BaseModel


class UserCreate(BaseModel):
    """
    Datos necesarios para crear un usuario.
    """

    nombre: str
    email: str
    password: str