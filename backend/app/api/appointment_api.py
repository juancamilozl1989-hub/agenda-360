# Router de FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Sesión de SQLAlchemy
from sqlalchemy.orm import Session

# Dependencia de la base de datos
from app.core.dependencies import get_db

# Modelos
from app.models.appointment_model import Appointment
from app.models.client_model import Client
from app.models.barber_model import Barber
from app.models.service_model import Service

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
    db: Session = Depends(get_db)
):
    """
    Registrar una nueva cita.
    """

    # Verificar cliente
    cliente = db.query(Client).filter(
        Client.id == datos.client_id
    ).first()

    if cliente is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    # Verificar barbero
    barbero = db.query(Barber).filter(
        Barber.id == datos.barber_id
    ).first()

    if barbero is None:
        raise HTTPException(
            status_code=404,
            detail="Barbero no encontrado"
        )

    # Verificar servicio
    servicio = db.query(Service).filter(
        Service.id == datos.service_id
    ).first()

    if servicio is None:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado"
        )

    # Crear cita
    cita = Appointment(
        fecha=datos.fecha,
        hora=datos.hora,
        client_id=datos.client_id,
        barber_id=datos.barber_id,
        service_id=datos.service_id
    )

    db.add(cita)
    db.commit()
    db.refresh(cita)

    return cita

# ==========================================
# Obtener todas las citas
# ==========================================
@router.get("/", response_model=list[AppointmentResponse])
def obtener_citas(
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
    db: Session = Depends(get_db)
):
    """
    Actualizar una cita.
    """

    cita = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if cita is None:
        raise HTTPException(
            status_code=404,
            detail="Cita no encontrada"
        )

    # Validar cliente
    cliente = db.query(Client).filter(
        Client.id == datos.client_id
    ).first()

    if cliente is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    # Validar barbero
    barbero = db.query(Barber).filter(
        Barber.id == datos.barber_id
    ).first()

    if barbero is None:
        raise HTTPException(
            status_code=404,
            detail="Barbero no encontrado"
        )

    # Validar servicio
    servicio = db.query(Service).filter(
        Service.id == datos.service_id
    ).first()

    if servicio is None:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado"
        )

    cita.fecha = datos.fecha
    cita.hora = datos.hora
    cita.estado = datos.estado
    cita.client_id = datos.client_id
    cita.barber_id = datos.barber_id
    cita.service_id = datos.service_id

    db.commit()
    db.refresh(cita)

    return cita

# ==========================================
# Eliminar una cita
# ==========================================
@router.delete("/{appointment_id}")
def eliminar_cita(
    appointment_id: int,
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