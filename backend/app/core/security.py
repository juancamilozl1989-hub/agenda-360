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