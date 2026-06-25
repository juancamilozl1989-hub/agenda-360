from pydantic import BaseModel


class UserCreate(BaseModel):
    """
    Datos necesarios para crear un usuario.
    """

    nombre: str
    email: str
    password: str
    
class UserResponse(BaseModel):
    """
    Datos que se devolverán al cliente.
    """

    id: int
    nombre: str
    email: str

    class Config:
        from_attributes = True