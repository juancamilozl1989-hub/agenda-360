# Permite obtener la conexión a la base de datos
from fastapi import APIRouter, Depends

# Tipo de sesión de SQLAlchemy
from sqlalchemy.orm import Session

# Dependencia para abrir/cerrar conexión
from app.core.dependencies import get_db

# Modelo de la tabla users
from app.models.user_model import User

# Esquema para validar datos de entrada
from app.schemas.user_schema import UserCreate, UserResponse


# Agrupador de rutas relacionadas con usuarios
router = APIRouter(prefix="/users", tags=["Usuarios"])


@router.post("/")
def crear_usuario(usuario: UserCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo usuario en PostgreSQL.
    """
        # Verificar si ya existe un usuario con ese correo
    usuario_existente = db.query(User).filter(
        User.email == usuario.email
    ).first()

    if usuario_existente:
        return {
            "mensaje": "El correo ya se encuentra registrado"
        }

    # Crear objeto User a partir de los datos recibidos
    nuevo_usuario = User(
        nombre=usuario.nombre,
        email=usuario.email,
        password=usuario.password
    )

    # Guardar en la base de datos
    db.add(nuevo_usuario)

    # Confirmar cambios
    db.commit()

    return {
        "mensaje": "Usuario creado correctamente"
    }
    
@router.get("/", response_model=list[UserResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    """
    Obtener todos los usuarios registrados.
    """

    usuarios = db.query(User).all()

    return usuarios