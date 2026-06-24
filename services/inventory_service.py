from sqlalchemy.orm import Session
from models.inventory_model import Inventory
from models.product_model import Product

def get_inventory(db: Session, product_id: int):
    return (db.query(Inventory).filter(Inventory.product_id == product_id).first())

def stock_in(db: Session, product_id: int, quantity: int):
    inventory = get_inventory(db, product_id)
    if not inventory:
        inventory = Inventory(product_id=product_id, quantity=quantity)
        db.add(inventory)
    else:
        inventory.quantity += quantity
    db.commit()
    db.refresh(inventory)
    return inventory


def stock_out(db: Session, product_id: int, quantity: int):
    inventory = get_inventory(db, product_id)
    if not inventory:
        raise Exception("Inventory not found")
    if inventory.quantity < quantity:
        raise Exception("Insufficient stock")
    inventory.quantity -= quantity
    db.commit()
    db.refresh(inventory)
    return inventory

def inventory_report(db: Session):
    return (db.query(Inventory).all())

def low_stock_report(db: Session, threshold: int = 10):
    return (db.query(Inventory).filter(Inventory.quantity <= threshold).all())

def inventory_statistics(db: Session):
    inventory = db.query(Inventory).all()
    total_products = len(inventory)
    total_quantity = sum(
        item.quantity
        for item in inventory)
    return {"total_products":total_products, "total_quantity": total_quantity}