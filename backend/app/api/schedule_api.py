# Router de FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Sesión de SQLAlchemy
from sqlalchemy.orm import Session

# Dependencia de la base de datos
from app.core.dependencies import get_db

# Modelos
from app.models.schedule_model import Schedule
from app.models.barber_model import Barber

# Schemas
from app.schemas.schedule_schema import (
    ScheduleCreate,
    ScheduleUpdate,
    ScheduleResponse
)

# Crear router
router = APIRouter(
    prefix="/schedules",
    tags=["Horarios"]
)

# ==========================================
# Crear un horario
# ==========================================
@router.post("/", response_model=ScheduleResponse)
def crear_horario(
    datos: ScheduleCreate,
    db: Session = Depends(get_db)
):
    """
    Registrar un nuevo horario para un barbero.
    """

    # Verificar que exista el barbero
    barbero = db.query(Barber).filter(
        Barber.id == datos.barber_id
    ).first()

    if barbero is None:
        raise HTTPException(
            status_code=404,
            detail="Barbero no encontrado"
        )

    # Crear horario
    horario = Schedule(
        dia_semana=datos.dia_semana,
        hora_inicio=datos.hora_inicio,
        hora_fin=datos.hora_fin,
        barber_id=datos.barber_id
    )

    # Guardar en la base de datos
    db.add(horario)
    db.commit()
    db.refresh(horario)

    return horario

# ==========================================
# Listar todos los horarios
# ==========================================
@router.get("/", response_model=list[ScheduleResponse])
def listar_horarios(
    db: Session = Depends(get_db)
):
    """
    Obtener todos los horarios registrados.
    """

    horarios = db.query(Schedule).all()

    return horarios

# ==========================================
# Obtener un horario por ID
# ==========================================
@router.get("/{schedule_id}", response_model=ScheduleResponse)
def obtener_horario(
    schedule_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener un horario específico.
    """

    horario = db.query(Schedule).filter(
        Schedule.id == schedule_id
    ).first()

    if horario is None:
        raise HTTPException(
            status_code=404,
            detail="Horario no encontrado"
        )

    return horario

# ==========================================
# Actualizar un horario
# ==========================================
@router.put("/{schedule_id}", response_model=ScheduleResponse)
def actualizar_horario(
    schedule_id: int,
    datos: ScheduleUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un horario.
    """

    horario = db.query(Schedule).filter(
        Schedule.id == schedule_id
    ).first()

    if horario is None:
        raise HTTPException(
            status_code=404,
            detail="Horario no encontrado"
        )

    barbero = db.query(Barber).filter(
        Barber.id == datos.barber_id
    ).first()

    if barbero is None:
        raise HTTPException(
            status_code=404,
            detail="Barbero no encontrado"
        )

    horario.dia_semana = datos.dia_semana
    horario.hora_inicio = datos.hora_inicio
    horario.hora_fin = datos.hora_fin
    horario.barber_id = datos.barber_id

    db.commit()
    db.refresh(horario)

    return horario

# ==========================================
# Eliminar un horario
# ==========================================
@router.delete("/{schedule_id}")
def eliminar_horario(
    schedule_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar un horario.
    """

    horario = db.query(Schedule).filter(
        Schedule.id == schedule_id
    ).first()

    if horario is None:
        raise HTTPException(
            status_code=404,
            detail="Horario no encontrado"
        )

    db.delete(horario)
    db.commit()

    return {
        "mensaje": "Horario eliminado correctamente"
    }