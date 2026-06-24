from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.permission import require_roles
from models.ticket_model import Ticket
from models.ticket_comment_model import TicketComment
from models.ticket_history_model import TicketHistory
from schemas.ticket_schema import TicketCreate, TicketAssign, TicketCommentCreate
from services.notification_service import create_notification

router = APIRouter(prefix="/tickets", tags=["Support Tickets"], dependencies=[Depends(require_roles("EMPLOYEE", "ADMIN", "SUPER_ADMIN", "HR", "MANAGER"))])


@router.post("/")
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    ticket = Ticket(**payload.model_dump())
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    history = TicketHistory(
        ticket_id=ticket.id,
        action="Ticket Created",
        performed_by=payload.created_by
    )
    db.add(history)
    db.commit()
    return {"message": "Ticket Created", "ticket_id": ticket.id}


@router.get("/")
def get_tickets(db: Session = Depends(get_db)):
    return db.query(Ticket).all()


@router.get("/{ticket_id}")
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.put("/{ticket_id}/assign")
def assign_ticket(ticket_id: int, payload: TicketAssign, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket.assigned_to = payload.assigned_to
    db.commit()
    create_notification(db, payload.assigned_to, "Ticket Assigned", f"Ticket #{ticket_id} assigned to you")
    history = TicketHistory(
        ticket_id=ticket_id,
        action=f"Assigned to user {payload.assigned_to}",
        performed_by=payload.assigned_to
    )
    db.add(history)
    db.commit()
    return {"message": "Ticket Assigned"}


@router.put("/{ticket_id}/status")
def update_status(ticket_id: int, status: str, user_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket.status = status
    db.commit()
    history = TicketHistory(
        ticket_id=ticket_id,
        action=f"Status changed to {status}",
        performed_by=user_id
    )
    db.add(history)
    db.commit()
    return {"message": "Status Updated"}


@router.post("/{ticket_id}/comment")
def add_comment(ticket_id: int, payload: TicketCommentCreate, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    comment = TicketComment(
        ticket_id=ticket_id,
        user_id=payload.user_id,
        comment=payload.comment
    )
    db.add(comment)
    db.commit()
    return {"message": "Comment Added"}


@router.get("/{ticket_id}/comments")
def get_comments(ticket_id: int, db: Session = Depends(get_db)):
    return db.query(TicketComment).filter(TicketComment.ticket_id == ticket_id).all()


@router.get("/{ticket_id}/history")
def get_history(ticket_id: int, db: Session = Depends(get_db)):
    return db.query(TicketHistory).filter(TicketHistory.ticket_id == ticket_id).all()