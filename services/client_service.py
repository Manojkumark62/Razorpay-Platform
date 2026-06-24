from sqlalchemy.orm import Session
from models.client_model import Client

def create_client(db: Session, payload):
    client = Client(**payload.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

def get_clients(db: Session):
    return db.query(Client).all()

def get_client(db: Session, client_id: int):
    return (db.query(Client).filter(Client.id == client_id).first())

def delete_client(db: Session, client_id: int):
    client = get_client(db, client_id)
    if not client:
        return False
    db.delete(client)
    db.commit()
    return True