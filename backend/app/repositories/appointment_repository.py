# Sesión de SQLAlchemy
from sqlalchemy.orm import Session

# Modelos
from app.models.appointment_model import Appointment
from app.models.client_model import Client
from app.models.barber_model import Barber
from app.models.service_model import Service


# ==========================================
# Obtener un cliente por ID
# ==========================================
def obtener_cliente(
    client_id: int,
    db: Session
):
    """
    Obtener un cliente por su ID.
    """

    return db.query(Client).filter(
        Client.id == client_id
    ).first()


# ==========================================
# Obtener un barbero por ID
# ==========================================
def obtener_barbero(
    barber_id: int,
    db: Session
):
    """
    Obtener un barbero por su ID.
    """

    return db.query(Barber).filter(
        Barber.id == barber_id
    ).first()


# ==========================================
# Obtener un servicio por ID
# ==========================================
def obtener_servicio(
    service_id: int,
    db: Session
):
    """
    Obtener un servicio por su ID.
    """

    return db.query(Service).filter(
        Service.id == service_id
    ).first()


# ==========================================
# Buscar cita duplicada
# ==========================================
def obtener_cita_duplicada(
    barber_id: int,
    fecha,
    hora,
    db: Session
):
    """
    Buscar si ya existe una cita para un
    barbero en la misma fecha y hora.
    """

    return db.query(Appointment).filter(
        Appointment.barber_id == barber_id,
        Appointment.fecha == fecha,
        Appointment.hora == hora
    ).first()


# ==========================================
# Guardar una cita
# ==========================================
def guardar_cita(
    cita: Appointment,
    db: Session
):
    """
    Guardar una cita en la base de datos.
    """

    db.add(cita)
    db.commit()
    db.refresh(cita)

    return cita