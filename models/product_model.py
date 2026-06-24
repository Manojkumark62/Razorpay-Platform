from sqlalchemy import Column, Integer, String, Float, ForeignKey
from core.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    description = Column(String(500))
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))