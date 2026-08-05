from sqlalchemy.orm import Session

from app.models.client_model import Client
from app.schemas.client_schema import ClientCreate, ClientUpdate


class ClientRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Client).all()

    @staticmethod
    def get_by_id(db: Session, client_id: int):
        return (
            db.query(Client)
            .filter(Client.id == client_id)
            .first()
        )

    @staticmethod
    def create(db: Session, client: ClientCreate):

        new_client = Client(
            nombre=client.nombre,
            telefono=client.telefono,
            email=client.email,
            estado=client.estado,
            barbershop_id=client.barbershop_id,
        )

        db.add(new_client)
        db.commit()
        db.refresh(new_client)

        return new_client

    @staticmethod
    def update(
        db: Session,
        client_id: int,
        data: ClientUpdate,
    ):

        client = (
            db.query(Client)
            .filter(Client.id == client_id)
            .first()
        )

        if not client:
            return None

        client.nombre = data.nombre
        client.telefono = data.telefono
        client.email = data.email
        client.estado = data.estado
        client.barbershop_id = data.barbershop_id

        db.commit()
        db.refresh(client)

        return client

    @staticmethod
    def delete(
        db: Session,
        client_id: int,
    ):

        client = (
            db.query(Client)
            .filter(Client.id == client_id)
            .first()
        )

        if not client:
            return False

        db.delete(client)
        db.commit()

        return True