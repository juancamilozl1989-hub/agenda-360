"""
Módulo de seguridad de Agenda 360.

Aquí se concentrarán todas las funciones relacionadas con:

- Encriptación de contraseñas.
- Verificación de contraseñas.
- Creación de tokens JWT.
- Validación de tokens.
"""

# Librería para encriptar contraseñas
from passlib.context import CryptContext

from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer


# ==========================================================
# Configuración del algoritmo de encriptación
# ==========================================================
#
# bcrypt es uno de los algoritmos más utilizados actualmente
# para almacenar contraseñas de forma segura.
#
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ==========================================================
# Encriptar una contraseña
# ==========================================================
def obtener_password_hash(password: str) -> str:
    """
    Convierte una contraseña en texto plano
    en un hash seguro.
    """
    return pwd_context.hash(password)


# ==========================================================
# Verificar una contraseña
# ==========================================================
def verificar_password(
    password_plano: str,
    password_hash: str
) -> bool:
    """
    Compara una contraseña ingresada por el usuario
    con la contraseña almacenada en la base de datos.
    """
    return pwd_context.verify(
        password_plano,
        password_hash
    )
    
SECRET_KEY = "agenda360_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login"
)

def crear_access_token(data: dict):
    """
    Genera un JWT.
    """

    datos = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    datos.update({"exp": expire})

    return jwt.encode(
        datos,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
def verificar_token(token: str):
    """
    Verifica que un JWT sea válido y devuelve su contenido.
    """

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )
        
from fastapi import Depends


def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme)
):
    """
    Obtiene la información contenida
    en el JWT del usuario autenticado.
    """

    return verificar_token(token)