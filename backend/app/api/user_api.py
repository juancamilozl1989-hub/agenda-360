# Permite obtener la conexión a la base de datos
from fastapi import APIRouter, Depends, HTTPException

# Tipo de sesión de SQLAlchemy
from sqlalchemy.orm import Session

# Dependencia para abrir/cerrar conexión
from app.core.dependencies import get_db

# Modelo de la tabla users
from app.models.user_model import User

# Esquema para validar datos de entrada
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse, UserLogin

from app.core.security import obtener_password_hash, verificar_password, crear_access_token, obtener_usuario_actual

from fastapi.security import OAuth2PasswordRequestForm

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
        password=obtener_password_hash(usuario.password)
    )

    # Guardar en la base de datos
    db.add(nuevo_usuario)

    # Confirmar cambios
    db.commit()

    return {
        "mensaje": "Usuario creado correctamente"
    }
    
@router.get("/", response_model=list[UserResponse])
def listar_usuarios(
    usuario_actual = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """
    Obtener todos los usuarios registrados.
    """

    usuarios = db.query(User).all()

    return usuarios

@router.get("/{user_id}", response_model=UserResponse)
def obtener_usuario(user_id: int, db: Session = Depends(get_db)):
    """
    Obtener un usuario específico por su ID.
    """

    # Buscar el usuario en la base de datos
    usuario = db.query(User).filter(User.id == user_id).first()

    # Si no existe, devolver un error 404
    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    # Si existe, devolver el usuario
    return usuario

# Actualizar un usuario por su ID
# ==========================================
@router.put("/{user_id}", response_model=UserResponse)
def actualizar_usuario(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    # Buscar el usuario en la base de datos
    user = db.query(User).filter(User.id == user_id).first()

    # Si no existe, devolver error 404
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualizar los datos del usuario
    user.nombre = user_data.nombre
    user.email = user_data.email

    # Guardar los cambios en la base de datos
    db.commit()

    # Refrescar el objeto para obtener la información actualizada
    db.refresh(user)

    # Retornar el usuario actualizado
    return user

# ==========================================
# Eliminar un usuario por su ID
# ==========================================
@router.delete("/{user_id}")
def eliminar_usuario(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina un usuario de la base de datos.
    """

    # Buscar el usuario por su ID
    usuario = db.query(User).filter(User.id == user_id).first()

    # Si no existe, devolver error 404
    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    # Eliminar el usuario
    db.delete(usuario)

    # Guardar los cambios en la base de datos
    db.commit()

    # Confirmar la eliminación
    return {
        "mensaje": "Usuario eliminado correctamente"
    }
    
# ==========================================
# Login de usuario
# ==========================================
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Verificar las credenciales de un usuario.
    """

    # Buscar usuario por correo (username contiene el email)
    usuario = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos"
        )

    if not verificar_password(
        form_data.password,
        usuario.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos"
        )

    access_token = crear_access_token(
        data={
            "sub": usuario.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }