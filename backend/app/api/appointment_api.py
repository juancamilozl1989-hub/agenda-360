# Router de FastAPI
from fastapi import APIRouter, Depends, HTTPException
from datetime import date

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
    # No permitir citas en fechas pasadas
    if datos.fecha < date.today():
        raise HTTPException(
            status_code=400,
            detail="No se pueden registrar citas en fechas pasadas."
    )

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
        
    # Verificar que el servicio pertenezca al barbero
    if servicio.barber_id != datos.barber_id:
        raise HTTPException(
            status_code=400,
            detail="El servicio seleccionado no pertenece al barbero."
    )
        
    # Verificar si el barbero ya tiene una cita
    # en esa misma fecha y hora
    cita_existente = db.query(Appointment).filter(
        Appointment.barber_id == datos.barber_id,
        Appointment.fecha == datos.fecha,
        Appointment.hora == datos.hora
    ).first()

    if cita_existente:
        raise HTTPException(
            status_code=400,
            detail="El barbero ya tiene una cita programada para esa fecha y hora."
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

    # No permitir actualizar una cita a una fecha pasada
    if datos.fecha < date.today():
        raise HTTPException(
            status_code=400,
            detail="No se pueden registrar citas en fechas pasadas."
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
        
    # Verificar que el servicio pertenezca al barbero
    if servicio.barber_id != datos.barber_id:
        raise HTTPException(
            status_code=400,
            detail="El servicio seleccionado no pertenece al barbero."
    )

    # Verificar que el barbero no tenga otra cita
    # en la misma fecha y hora
    cita_existente = db.query(Appointment).filter(
        Appointment.barber_id == datos.barber_id,
        Appointment.fecha == datos.fecha,
        Appointment.hora == datos.hora,
        Appointment.id != appointment_id
    ).first()

    if cita_existente:
        raise HTTPException(
            status_code=400,
            detail="El barbero ya tiene una cita programada para esa fecha y hora."
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