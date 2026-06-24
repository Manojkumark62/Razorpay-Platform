from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.permission import require_roles
from core.response import success_response
from models.inventory_model import Inventory
from models.product_model import Product

router = APIRouter(prefix="/inventory", tags=["Inventory"], dependencies=[Depends(require_roles("ADMIN", "SUPER_ADMIN", "HR", "MANAGER"))])


@router.post("/stock-in/{product_id}")
def stock_in(product_id: int, quantity: int, db: Session = Depends(get_db)):
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not inventory:
        inventory = Inventory(product_id=product_id, quantity=quantity)
        db.add(inventory)
    else:
        inventory.quantity += quantity

    db.commit()
    db.refresh(inventory)
    return success_response(
        "Stock added successfully",
        {"product_id": inventory.product_id, "current_quantity": inventory.quantity},
    )


@router.post("/stock-out/{product_id}")
def stock_out(product_id: int, quantity: int, db: Session = Depends(get_db)):
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Product not found in inventory")
    if inventory.quantity < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    inventory.quantity -= quantity
    db.commit()
    db.refresh(inventory)
    return success_response(
        "Stock removed successfully",
        {"product_id": inventory.product_id, "current_quantity": inventory.quantity},
    )


@router.get("/report")
def inventory_report(db: Session = Depends(get_db)):
    inventory_items = db.query(Inventory).all()
    data = [{"product_id": item.product_id, "quantity": item.quantity} for item in inventory_items]
    return success_response("Inventory report fetched successfully", data)


@router.get("/{product_id}")
def get_stock(product_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Product not found in inventory")

    return success_response(
        "Inventory fetched successfully",
        {"product_id": inventory.product_id, "quantity": inventory.quantity},
    )
