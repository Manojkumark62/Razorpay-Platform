from pydantic import BaseModel

class TicketCreate(BaseModel):
    title: str
    description: str
    created_by: int
    priority: str

class TicketAssign(BaseModel):
    assigned_to: int

class TicketCommentCreate(BaseModel):
    user_id: int
    comment: str