from pydantic import BaseModel

class SupplierCreate(BaseModel):
    name: str
    email: str
    phone: str
    address: str