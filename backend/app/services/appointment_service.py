# Fecha
from datetime import date

# Excepciones de FastAPI
from fastapi import HTTPException

# Sesión de SQLAlchemy
from sqlalchemy.orm import Session

# Modelos
from app.models.appointment_model import Appointment

# Repository
from app.repositories import appointment_repository

# Schemas
from app.schemas.appointment_schema import AppointmentCreate


# ==========================================
# Crear una cita
# ==========================================
def crear_cita(
    datos: AppointmentCreate,
    db: Session
):
    """
    Contiene la lógica de negocio para registrar una cita.
    """

    # No permitir citas en fechas pasadas
    if datos.fecha < date.today():
        raise HTTPException(
            status_code=400,
            detail="No se pueden registrar citas en fechas pasadas."
        )

    # Verificar cliente
    cliente = appointment_repository.obtener_cliente(
        datos.client_id,
        db
    )

    if cliente is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    # Verificar barbero
    barbero = appointment_repository.obtener_barbero(
        datos.barber_id,
        db
    )

    if barbero is None:
        raise HTTPException(
            status_code=404,
            detail="Barbero no encontrado"
        )

    # Verificar servicio
    servicio = appointment_repository.obtener_servicio(
        datos.service_id,
        db
    )

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

    # Verificar cita duplicada
    cita_existente = appointment_repository.obtener_cita_duplicada(
        datos.barber_id,
        datos.fecha,
        datos.hora,
        db
    )

    if cita_existente:
        raise HTTPException(
            status_code=400,
            detail="El barbero ya tiene una cita programada para esa fecha y hora."
        )

    # Crear objeto
    cita = Appointment(
        fecha=datos.fecha,
        hora=datos.hora,
        client_id=datos.client_id,
        barber_id=datos.barber_id,
        service_id=datos.service_id
    )

    # Guardar mediante Repository
    return appointment_repository.guardar_cita(
        cita,
        db
    )


# ==========================================
# Obtener todas las citas
# ==========================================
def obtener_citas(
    db: Session
):
    """
    Obtener todas las citas.
    """

    return db.query(Appointment).all()


# ==========================================
# Obtener una cita por ID
# ==========================================
def obtener_cita(
    appointment_id: int,
    db: Session
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