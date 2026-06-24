from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.product_model import Product

def create_product(db: Session, payload):
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_product(db: Session, product_id: int):
    return (db.query(Product).filter(Product.id == product_id).first())

def get_products(db: Session):
    return (db.query(Product).all())

def update_product(db: Session, product_id: int, payload):
    product = get_product(db, product_id)
    if not product:
        return None
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if not product:
        return False
    db.delete(product)
    db.commit()
    return True

def search_products(db: Session, keyword: str):
    return (db.query(Product).filter(or_(Product.name.ilike(f"%{keyword}%"), Product.description.ilike(f"%{keyword}%"))).all())