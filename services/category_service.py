from sqlalchemy.orm import Session
from models.category_model import Category

def create_category(db: Session, payload):
    category = Category(**payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_category(db: Session, category_id: int):
    return (db.query(Category).filter(Category.id == category_id).first())

def get_categories(db: Session):
    return (db.query(Category).all())

def update_category(db: Session, category_id: int, payload):
    category = get_category(db, category_id)
    if not category:
        return None
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category

def delete_category(db: Session, category_id: int):
    category = get_category(db, category_id)
    if not category:
        return False
    db.delete(category)
    db.commit()
    return True