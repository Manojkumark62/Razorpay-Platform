from pydantic import BaseModel

class DesignationCreate(BaseModel):
    title: str
    description: str