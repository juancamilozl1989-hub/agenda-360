# Permite crear rutas y manejar errores
from fastapi import APIRouter, Depends, HTTPException

# Sesión de SQLAlchemy
from sqlalchemy.orm import Session

# Conexión a la base de datos
from app.core.dependencies import get_db

# Modelos
from app.models.barber_model import Barber
from app.models.barbershop_model import Barbershop

# Schemas
from app.schemas.barber_schema import (
    BarberCreate,
    BarberResponse,
    BarberUpdate
)

# Router
router = APIRouter(
    prefix="/barbers",
    tags=["Barberos"]
)


# ==========================================
# Crear un barbero
# ==========================================
@router.post("/", response_model=BarberResponse)
def crear_barbero(
    barbero: BarberCreate,
    db: Session = Depends(get_db)
):
    """
    Registrar un nuevo barbero.
    """

    # Verificar que la barbería exista
    barberia = db.query(Barbershop).filter(
        Barbershop.id == barbero.barbershop_id
    ).first()

    if barberia is None:
        raise HTTPException(
            status_code=404,
            detail="La barbería no existe"
        )

    # Crear el barbero
    nuevo_barbero = Barber(
        nombre=barbero.nombre,
        telefono=barbero.telefono,
        barbershop_id=barbero.barbershop_id
    )

    db.add(nuevo_barbero)
    db.commit()
    db.refresh(nuevo_barbero)

    return nuevo_barbero

# ==========================================
# Listar todos los barberos
# ==========================================
@router.get("/", response_model=list[BarberResponse])
def listar_barberos(
    db: Session = Depends(get_db)
):
    """
    Obtener todos los barberos registrados.
    """

    barberos = db.query(Barber).all()

    return barberos

# ==========================================
# Obtener un barbero por su ID
# ==========================================
@router.get("/{barber_id}", response_model=BarberResponse)
def obtener_barbero(
    barber_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener un barbero específico por su ID.
    """

    # Buscar el barbero
    barbero = db.query(Barber).filter(
        Barber.id == barber_id
    ).first()

    # Validar si existe
    if barbero is None:
        raise HTTPException(
            status_code=404,
            detail="Barbero no encontrado"
        )

    return barbero

# ==========================================
# Actualizar un barbero
# ==========================================
@router.put("/{barber_id}", response_model=BarberResponse)
def actualizar_barbero(
    barber_id: int,
    datos: BarberUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar la información de un barbero.
    """

    # Buscar el barbero
    barbero = db.query(Barber).filter(
        Barber.id == barber_id
    ).first()

    # Verificar si existe
    if barbero is None:
        raise HTTPException(
            status_code=404,
            detail="Barbero no encontrado"
        )

    # Verificar que la barbería exista
    barberia = db.query(Barbershop).filter(
        Barbershop.id == datos.barbershop_id
    ).first()

    if barberia is None:
        raise HTTPException(
            status_code=404,
            detail="La barbería no existe"
        )

    # Actualizar los datos
    barbero.nombre = datos.nombre
    barbero.telefono = datos.telefono
    barbero.barbershop_id = datos.barbershop_id

    db.commit()
    db.refresh(barbero)

    return barbero

# ==========================================
# Eliminar un barbero
# ==========================================
@router.delete("/{barber_id}")
def eliminar_barbero(
    barber_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar un barbero.
    """

    # Buscar el barbero
    barbero = db.query(Barber).filter(
        Barber.id == barber_id
    ).first()

    # Validar que exista
    if barbero is None:
        raise HTTPException(
            status_code=404,
            detail="Barbero no encontrado"
        )

    # Eliminar
    db.delete(barbero)
    db.commit()

    return {
        "mensaje": "Barbero eliminado correctamente"
    }