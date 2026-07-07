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
    BarberResponse
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