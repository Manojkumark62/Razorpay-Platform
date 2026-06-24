from pydantic import BaseModel

class LeadCreate(BaseModel):
    client_name: str
    email: str
    phone: str
    source: str