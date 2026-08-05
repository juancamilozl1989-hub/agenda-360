from sqlalchemy.orm import Session

from app.repositories.client_repository import ClientRepository
from app.schemas.client_schema import ClientCreate, ClientUpdate


class ClientService:

    @staticmethod
    def get_all(db: Session):
        return ClientRepository.get_all(db)

    @staticmethod
    def get_by_id(db: Session, client_id: int):
        return ClientRepository.get_by_id(db, client_id)

    @staticmethod
    def create(db: Session, client: ClientCreate):
        return ClientRepository.create(db, client)

    @staticmethod
    def update(
        db: Session,
        client_id: int,
        client: ClientUpdate,
    ):
        return ClientRepository.update(
            db,
            client_id,
            client,
        )

    @staticmethod
    def delete(
        db: Session,
        client_id: int,
    ):
        return ClientRepository.delete(
            db,
            client_id,
        )