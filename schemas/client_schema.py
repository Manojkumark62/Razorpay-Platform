from pydantic import BaseModel

class ClientCreate(BaseModel):
    company_name: str
    contact_person: str
    email: str
    phone: str
    address: str