# Fecha
from datetime import date

# Router de FastAPI
from fastapi import APIRouter, Depends, Query

# Sesión de SQLAlchemy
from sqlalchemy.orm import Session

# Dependencias
from app.core.dependencies import get_db
from app.core.security import obtener_usuario_actual

# Lógica de negocio
from app.services import appointment_service

# Schemas
from app.schemas.availability_schema import AvailabilityResponse

# Crear router
router = APIRouter(
    prefix="/availability",
    tags=["Disponibilidad"]
)


# ==========================================
# Consultar horas disponibles
# ==========================================
@router.get("/", response_model=AvailabilityResponse)
def consultar_disponibilidad(
    fecha: date = Query(..., description="Fecha a consultar (AAAA-MM-DD)"),
    service_id: int = Query(..., description="Servicio que se quiere agendar"),
    barber_id: int | None = Query(
        None,
        description="Barbero preferido. Si se omite, se revisan todos los barberos activos."
    ),
    usuario_actual = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """
    Devuelve las horas libres para un servicio en una fecha, según los
    horarios habilitados de los barberos y las citas ya registradas.

    Es la consulta que usará el bot de WhatsApp para ofrecer turnos al
    cliente. Cada hora trae la lista de barberos libres en ese momento.
    """

    return appointment_service.calcular_disponibilidad(
        fecha,
        service_id,
        db,
        barber_id
    )
