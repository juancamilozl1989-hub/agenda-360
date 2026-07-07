from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db

from app.models.barbershop_model import Barbershop

from app.schemas.barbershop_schema import (
    BarbershopCreate,
    BarbershopUpdate,
    BarbershopResponse
)

router = APIRouter(
    prefix="/barbershops",
    tags=["Barberías"]
)


# ==========================================
# Crear barbería
# ==========================================
@router.post("/")
def crear_barberia(
    barberia: BarbershopCreate,
    db: Session = Depends(get_db)
):

    nueva_barberia = Barbershop(
        nombre=barberia.nombre,
        direccion=barberia.direccion,
        telefono=barberia.telefono,
        email=barberia.email
    )

    db.add(nueva_barberia)
    db.commit()

    return {
        "mensaje": "Barbería creada correctamente"
    }


# ==========================================
# Listar barberías
# ==========================================
@router.get("/", response_model=list[BarbershopResponse])
def listar_barberias(
    db: Session = Depends(get_db)
):

    return db.query(Barbershop).all()


# ==========================================
# Obtener barbería por ID
# ==========================================
@router.get("/{barbershop_id}", response_model=BarbershopResponse)
def obtener_barberia(
    barbershop_id: int,
    db: Session = Depends(get_db)
):

    barberia = db.query(Barbershop).filter(
        Barbershop.id == barbershop_id
    ).first()

    if barberia is None:
        raise HTTPException(
            status_code=404,
            detail="Barbería no encontrada"
        )

    return barberia


# ==========================================
# Actualizar barbería
# ==========================================
@router.put("/{barbershop_id}", response_model=BarbershopResponse)
def actualizar_barberia(
    barbershop_id: int,
    datos: BarbershopUpdate,
    db: Session = Depends(get_db)
):

    barberia = db.query(Barbershop).filter(
        Barbershop.id == barbershop_id
    ).first()

    if barberia is None:
        raise HTTPException(
            status_code=404,
            detail="Barbería no encontrada"
        )

    barberia.nombre = datos.nombre
    barberia.direccion = datos.direccion
    barberia.telefono = datos.telefono
    barberia.email = datos.email

    db.commit()
    db.refresh(barberia)

    return barberia


# ==========================================
# Eliminar barbería
# ==========================================
@router.delete("/{barbershop_id}")
def eliminar_barberia(
    barbershop_id: int,
    db: Session = Depends(get_db)
):

    barberia = db.query(Barbershop).filter(
        Barbershop.id == barbershop_id
    ).first()

    if barberia is None:
        raise HTTPException(
            status_code=404,
            detail="Barbería no encontrada"
        )

    db.delete(barberia)
    db.commit()

    return {
        "mensaje": "Barbería eliminada correctamente"
    }