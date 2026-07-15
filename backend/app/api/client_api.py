# Router de FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Sesión de SQLAlchemy
from sqlalchemy.orm import Session

# Dependencia de la base de datos
from app.core.dependencies import get_db

# Modelos
from app.models.client_model import Client
from app.models.barbershop_model import Barbershop

# Schemas
from app.schemas.client_schema import (
    ClientCreate,
    ClientUpdate,
    ClientResponse
)

# Crear router
router = APIRouter(
    prefix="/clients",
    tags=["Clientes"]
)

# ==========================================
# Crear un cliente
# ==========================================
@router.post("/", response_model=ClientResponse)
def crear_cliente(
    datos: ClientCreate,
    db: Session = Depends(get_db)
):
    """
    Registrar un nuevo cliente.
    """

    # Verificar que exista la barbería
    barberia = db.query(Barbershop).filter(
        Barbershop.id == datos.barbershop_id
    ).first()

    if barberia is None:
        raise HTTPException(
            status_code=404,
            detail="Barbería no encontrada"
        )

    # Crear cliente
    cliente = Client(
        nombre=datos.nombre,
        telefono=datos.telefono,
        email=datos.email,
        barbershop_id=datos.barbershop_id
    )

    # Guardar en la base de datos
    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    return cliente

# ==========================================
# Obtener todos los clientes
# ==========================================
@router.get("/", response_model=list[ClientResponse])
def obtener_clientes(
    db: Session = Depends(get_db)
):
    """
    Obtener todos los clientes.
    """

    clientes = db.query(Client).all()

    return clientes

# ==========================================
# Obtener un cliente por ID
# ==========================================
@router.get("/{client_id}", response_model=ClientResponse)
def obtener_cliente(
    client_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener un cliente específico.
    """

    cliente = db.query(Client).filter(
        Client.id == client_id
    ).first()

    if cliente is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    return cliente

# ==========================================
# Actualizar un cliente
# ==========================================
@router.put("/{client_id}", response_model=ClientResponse)
def actualizar_cliente(
    client_id: int,
    datos: ClientUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un cliente.
    """

    cliente = db.query(Client).filter(
        Client.id == client_id
    ).first()

    if cliente is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    barberia = db.query(Barbershop).filter(
        Barbershop.id == datos.barbershop_id
    ).first()

    if barberia is None:
        raise HTTPException(
            status_code=404,
            detail="Barbería no encontrada"
        )

    cliente.nombre = datos.nombre
    cliente.telefono = datos.telefono
    cliente.email = datos.email
    cliente.barbershop_id = datos.barbershop_id

    db.commit()
    db.refresh(cliente)

    return cliente

# ==========================================
# Eliminar un cliente
# ==========================================
@router.delete("/{client_id}")
def eliminar_cliente(
    client_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar un cliente.
    """

    cliente = db.query(Client).filter(
        Client.id == client_id
    ).first()

    if cliente is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    db.delete(cliente)
    db.commit()

    return {
        "mensaje": "Cliente eliminado correctamente"
    }