# Router de FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Sesión de SQLAlchemy
from sqlalchemy.orm import Session

# Dependencia de la base de datos
from app.core.dependencies import get_db
from app.core.security import obtener_usuario_actual

# Modelos
from app.models.appointment_model import Appointment

# Services
from app.services import appointment_service

# Schemas
from app.schemas.appointment_schema import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse
)

# Crear router
router = APIRouter(
    prefix="/appointments",
    tags=["Citas"]
)

# ==========================================
# Crear una cita
# ==========================================
@router.post("/", response_model=AppointmentResponse)
def crear_cita(
    datos: AppointmentCreate,
    usuario_actual = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """
    Registrar una nueva cita.
    """

    return appointment_service.crear_cita(
        datos,
        db
    )
      
@router.get("/", response_model=list[AppointmentResponse])
def obtener_citas(
    usuario_actual = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """
    Obtener todas las citas.
    """

    citas = db.query(Appointment).all()

    return citas

# ==========================================
# Obtener una cita por ID
# ==========================================
@router.get("/{appointment_id}", response_model=AppointmentResponse)
def obtener_cita(
    appointment_id: int,
    usuario_actual = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """
    Obtener una cita específica.
    """

    cita = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if cita is None:
        raise HTTPException(
            status_code=404,
            detail="Cita no encontrada"
        )

    return cita

# ==========================================
# Actualizar una cita
# ==========================================
@router.put("/{appointment_id}", response_model=AppointmentResponse)
def actualizar_cita(
    appointment_id: int,
    datos: AppointmentUpdate,
    usuario_actual = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """
    Actualizar una cita (reprogramar, cambiar de barbero o
    servicio, o cambiar su estado). Las reglas de negocio
    están en appointment_service.actualizar_cita.
    """

    return appointment_service.actualizar_cita(
        appointment_id,
        datos,
        db
    )

# ==========================================
# Eliminar una cita
# ==========================================
@router.delete("/{appointment_id}")
def eliminar_cita(
    appointment_id: int,
    usuario_actual = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """
    Eliminar una cita.
    """

    cita = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if cita is None:
        raise HTTPException(
            status_code=404,
            detail="Cita no encontrada"
        )

    db.delete(cita)
    db.commit()

    return {
        "mensaje": "Cita eliminada correctamente"
    }