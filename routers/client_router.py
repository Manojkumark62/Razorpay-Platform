from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.permission import require_roles
from models.client_model import Client
from schemas.client_schema import ClientCreate

router = APIRouter(prefix="/clients", tags=["Clients"], dependencies=[Depends(require_roles("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"))])

@router.post("/")
def create_client(payload: ClientCreate, db: Session = Depends(get_db)):
    client = Client(**payload.model_dump())
    db.add(client)
    db.commit()
    return {"Info": "Client Created"}

@router.get("/")
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

