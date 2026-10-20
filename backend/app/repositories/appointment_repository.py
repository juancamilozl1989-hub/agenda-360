# Fecha
from datetime import date

# Sesión de SQLAlchemy
from sqlalchemy.orm import Session

# Modelos
from app.models.appointment_model import Appointment
from app.models.client_model import Client
from app.models.barber_model import Barber
from app.models.service_model import Service
from app.models.schedule_model import Schedule


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
# Obtener los barberos activos
# ==========================================
def obtener_barberos_activos(
    db: Session
):
    """
    Barberos que pueden recibir citas.
    """

    return db.query(Barber).filter(
        Barber.estado == "Activo"
    ).order_by(Barber.nombre).all()


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
# Obtener una cita por ID
# ==========================================
def obtener_cita(
    appointment_id: int,
    db: Session
):
    """
    Obtener una cita por su ID.
    """

    return db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()


# ==========================================
# Horarios de un barbero para un día
# ==========================================
def obtener_horarios_del_dia(
    barber_id: int,
    dia_semana: str,
    db: Session
):
    """
    Bloques de atención que el barbero tiene habilitados
    para un día de la semana (puede tener varios, por
    ejemplo mañana y tarde).
    """

    return db.query(Schedule).filter(
        Schedule.barber_id == barber_id,
        Schedule.dia_semana == dia_semana
    ).order_by(Schedule.hora_inicio).all()


# ==========================================
# Citas activas de un barbero en una fecha
# ==========================================
def obtener_citas_activas_del_barbero(
    barber_id: int,
    fecha: date,
    db: Session,
    excluir_id: int | None = None
):
    """
    Citas que ocupan la agenda del barbero en una fecha.

    Las citas canceladas no cuentan: al cancelarse liberan
    el horario del barbero (hallazgo H-01). Al reprogramar
    una cita se excluye a ella misma para que no choque
    consigo misma.
    """

    consulta = db.query(Appointment).filter(
        Appointment.barber_id == barber_id,
        Appointment.fecha == fecha,
        Appointment.estado != "Cancelada"
    )

    if excluir_id is not None:
        consulta = consulta.filter(Appointment.id != excluir_id)

    return consulta.all()


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
