from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.permission import require_roles
from models.product_model import Product
from schemas.product_schema import ProductCreate

router = APIRouter(prefix="/products", tags=["Products"], dependencies=[Depends(require_roles("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"))])

@router.post("/")
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    return {"Info": "Product Created"}

@router.get("/")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()