# Router de FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Sesión de SQLAlchemy
from sqlalchemy.orm import Session

# Dependencia de la base de datos
from app.core.dependencies import get_db
from app.core.security import obtener_usuario_actual

# Modelos
from app.models.schedule_model import Schedule
from app.models.barber_model import Barber

# Schemas
from app.schemas.schedule_schema import (
    ScheduleCreate,
    ScheduleUpdate,
    ScheduleResponse
)

# Utilidades de agenda
from app.utils.agenda import DIAS_SEMANA, normalizar_dia


# ==========================================
# Validar los datos de un horario
# ==========================================
def validar_horario(datos, db: Session, excluir_id: int | None = None) -> str:
    """
    Comprueba el día y las horas del horario y que no se cruce con
    otro bloque del mismo barbero ese día. Devuelve el nombre oficial
    del día ("miercoles" -> "Miércoles").
    """

    dia = normalizar_dia(datos.dia_semana)

    if dia is None:
        raise HTTPException(
            status_code=400,
            detail="Día no válido. Use: " + ", ".join(DIAS_SEMANA) + "."
        )

    if datos.hora_fin <= datos.hora_inicio:
        raise HTTPException(
            status_code=400,
            detail="La hora de fin debe ser posterior a la hora de inicio."
        )

    otros = db.query(Schedule).filter(
        Schedule.barber_id == datos.barber_id,
        Schedule.dia_semana == dia
    )

    if excluir_id is not None:
        otros = otros.filter(Schedule.id != excluir_id)

    for otro in otros.all():
        if datos.hora_inicio < otro.hora_fin and otro.hora_inicio < datos.hora_fin:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"El horario se cruza con otro bloque del barbero el {dia.lower()} "
                    f"({otro.hora_inicio.strftime('%H:%M')} a {otro.hora_fin.strftime('%H:%M')})."
                )
            )

    return dia


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
    usuario_actual = Depends(obtener_usuario_actual),
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

    # Validar día, horas y cruces con otros bloques
    dia = validar_horario(datos, db)

    # Crear horario
    horario = Schedule(
        dia_semana=dia,
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
    usuario_actual = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """
    Obtener todos los horarios registrados.
    """

    horarios = db.query(Schedule).order_by(
        Schedule.barber_id,
        Schedule.hora_inicio
    ).all()

    return horarios

# ==========================================
# Obtener un horario por ID
# ==========================================
@router.get("/{schedule_id}", response_model=ScheduleResponse)
def obtener_horario(
    schedule_id: int,
    usuario_actual = Depends(obtener_usuario_actual),
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
    usuario_actual = Depends(obtener_usuario_actual),
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

    dia = validar_horario(datos, db, excluir_id=schedule_id)

    horario.dia_semana = dia
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
    usuario_actual = Depends(obtener_usuario_actual),
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