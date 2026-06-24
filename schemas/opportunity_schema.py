from pydantic import BaseModel

class OpportunityCreate(BaseModel):
    lead_id: int
    title: str
    value: float