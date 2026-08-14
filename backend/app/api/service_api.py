# Router de FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Sesión de SQLAlchemy
from sqlalchemy.orm import Session

# Dependencia para la base de datos
from app.core.dependencies import get_db

# Modelo Service
from app.models.service_model import Service

# Modelo Barber (para validar que exista)
from app.models.barber_model import Barber

# Schemas
from app.schemas.service_schema import (
    ServiceCreate,
    ServiceUpdate,
    ServiceResponse
)

# Crear router
router = APIRouter(
    prefix="/services",
    tags=["Servicios"]
)


# ==========================================
# Crear un servicio
# ==========================================
@router.post(
    "/",
    response_model=ServiceResponse
)
def crear_servicio(
    datos: ServiceCreate,
    db: Session = Depends(get_db)
):
    """
    Registrar un nuevo servicio.
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

    # Validar que el precio sea mayor que cero
    if datos.precio <= 0:
        raise HTTPException(
            status_code=400,
            detail="El precio del servicio debe ser mayor que cero."
        )

    # Validar que la duración sea mayor que cero
    if datos.duracion <= 0:
        raise HTTPException(
            status_code=400,
            detail="La duración del servicio debe ser mayor que cero."
        )

    # Validar el estado
    if datos.estado not in ["Activo", "Inactivo"]:
        raise HTTPException(
            status_code=400,
            detail="El estado debe ser 'Activo' o 'Inactivo'."
        )

    # Crear el servicio
    servicio = Service(
        nombre=datos.nombre,
        categoria=datos.categoria,
        descripcion=datos.descripcion,
        precio=datos.precio,
        duracion=datos.duracion,
        estado=datos.estado,
        barber_id=datos.barber_id
    )

    # Guardar en la base de datos
    db.add(servicio)
    db.commit()
    db.refresh(servicio)

    return servicio


# ==========================================
# Listar todos los servicios
# ==========================================
@router.get(
    "/",
    response_model=list[ServiceResponse]
)
def listar_servicios(
    db: Session = Depends(get_db)
):
    """
    Obtener todos los servicios registrados.
    """

    servicios = db.query(Service).all()

    return servicios


# ==========================================
# Obtener un servicio por ID
# ==========================================
@router.get(
    "/{service_id}",
    response_model=ServiceResponse
)
def obtener_servicio(
    service_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener un servicio específico.
    """

    servicio = db.query(Service).filter(
        Service.id == service_id
    ).first()

    if servicio is None:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado"
        )

    return servicio


# ==========================================
# Actualizar un servicio
# ==========================================
@router.put(
    "/{service_id}",
    response_model=ServiceResponse
)
def actualizar_servicio(
    service_id: int,
    datos: ServiceUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar la información de un servicio.
    """

    # Buscar el servicio
    servicio = db.query(Service).filter(
        Service.id == service_id
    ).first()

    if servicio is None:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado"
        )

    # Verificar que exista el barbero
    barbero = db.query(Barber).filter(
        Barber.id == datos.barber_id
    ).first()

    if barbero is None:
        raise HTTPException(
            status_code=404,
            detail="Barbero no encontrado"
        )

    # Validar que el precio sea mayor que cero
    if datos.precio <= 0:
        raise HTTPException(
            status_code=400,
            detail="El precio del servicio debe ser mayor que cero."
        )

    # Validar que la duración sea mayor que cero
    if datos.duracion <= 0:
        raise HTTPException(
            status_code=400,
            detail="La duración del servicio debe ser mayor que cero."
        )

    # Validar el estado
    if datos.estado not in ["Activo", "Inactivo"]:
        raise HTTPException(
            status_code=400,
            detail="El estado debe ser 'Activo' o 'Inactivo'."
        )

    # Actualizar datos
    servicio.nombre = datos.nombre
    servicio.categoria = datos.categoria
    servicio.descripcion = datos.descripcion
    servicio.precio = datos.precio
    servicio.duracion = datos.duracion
    servicio.estado = datos.estado
    servicio.barber_id = datos.barber_id

    # Guardar cambios
    db.commit()
    db.refresh(servicio)

    return servicio


# ==========================================
# Eliminar un servicio
# ==========================================
@router.delete("/{service_id}")
def eliminar_servicio(
    service_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar un servicio.
    """

    # Buscar el servicio
    servicio = db.query(Service).filter(
        Service.id == service_id
    ).first()

    if servicio is None:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado"
        )

    # Eliminar
    db.delete(servicio)
    db.commit()

    return {
        "mensaje": "Servicio eliminado correctamente"
    }