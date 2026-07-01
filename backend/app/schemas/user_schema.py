from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """
    Datos necesarios para crear un usuario.
    """

    nombre: str
    email: str
    password: str
    
# ==========================================
# Esquema para actualizar un usuario
# ==========================================
# En el futuro podremos agregar validaciones
# diferentes a las del registro.
class UserUpdate(BaseModel):
    nombre: str
    email: EmailStr 
    
class UserResponse(BaseModel):
    """
    Datos que se devolverán al cliente.
    """

    id: int
    nombre: str
    email: str

    class Config:
        from_attributes = True
        
class UserLogin(BaseModel):
    """
    Datos necesarios para iniciar sesión.
    """

    email: EmailStr
    password: str