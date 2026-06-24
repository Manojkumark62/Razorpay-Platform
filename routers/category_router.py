from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.permission import require_roles
from models.category_model import Category
from schemas.category_schema import CategoryCreate

router = APIRouter(prefix="/categories", tags=["Categories"], dependencies=[Depends(require_roles("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"))])

@router.post("/")
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    category = Category(**payload.model_dump())
    db.add(category)
    db.commit()
    return {"Info": "Category Created"}

@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()