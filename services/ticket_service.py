from sqlalchemy.orm import Session
from models.ticket_model import Ticket
from models.ticket_comment_model import TicketComment
from models.ticket_history_model import TicketHistory

def create_ticket(db: Session, payload):
    ticket = Ticket(**payload.model_dump())
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    history = TicketHistory(ticket_id=ticket.id, action="Ticket Created", performed_by=payload.created_by)
    db.add(history)
    db.commit()
    return ticket

def assign_ticket(db: Session, ticket_id: int, assigned_to: int):
    ticket = (db.query(Ticket).filter(Ticket.id == ticket_id).first())
    if not ticket:
        return None
    ticket.assigned_to = assigned_to
    db.commit()
    history = TicketHistory(ticket_id=ticket.id, action=f"Assigned to {assigned_to}", performed_by=assigned_to)
    db.add(history)
    db.commit()
    return ticket

def change_ticket_status(db: Session, ticket_id: int, status: str, user_id: int):
    ticket = (db.query(Ticket).filter(Ticket.id == ticket_id).first())
    if not ticket:
        return None
    ticket.status = status
    db.commit()
    history = TicketHistory(ticket_id=ticket.id, action=f"Status changed to {status}", performed_by=user_id)
    db.add(history)
    db.commit()
    return ticket

def add_comment(db: Session, ticket_id: int, user_id: int, comment: str):
    ticket_comment = TicketComment(ticket_id=ticket_id, user_id=user_id, comment=comment)
    db.add(ticket_comment)
    db.commit()
    db.refresh(ticket_comment)
    return ticket_comment

def get_ticket_history(db: Session, ticket_id: int):
    return (db.query(TicketHistory).filter(TicketHistory.ticket_id == ticket_id).all())