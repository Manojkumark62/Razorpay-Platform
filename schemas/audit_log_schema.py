from pydantic import BaseModel
from datetime import datetime

class AuditResponse(BaseModel):

    id: int
    user_id: int
    action: str
    entity: str
    entity_id: int | None
    ip_address: str | None
    created_at: datetime

    class Config:
        from_attributes = True