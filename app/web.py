from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse 
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models

from app.services import ticket_service 

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/entry-redirect/{gate_id}")
def scan_qr_entry(gate_id: int, db: Session = Depends(get_db)):

    db_session = ticket_service.create_ticket(db=db, gate_id=gate_id)
    
    if not db_session:
        return "HẾT CHỖ"

    plain_pass = getattr(db_session, "passcode_plain_for_response", "******")
    
    return RedirectResponse(
        url=f"/ticket/{db_session.session_id}?show_pass={plain_pass}", 
        status_code=303
    )

@router.get("/ticket/{session_id}")
def view_ticket(request: Request, session_id: str, db: Session = Depends(get_db), show_pass: str = None):
    session = db.query(models.ParkingTicketSession).filter(
        models.ParkingTicketSession.session_id == session_id
    ).first()
    
    if show_pass:
        display_passcode = show_pass
    else:
        display_passcode = "****** (Đã ẩn)"

    verify_link = str(request.url_for("view_verify_page", session_id=session_id))

    return templates.TemplateResponse("ticket.html", {
        "request": request,
        "session_id": session_id,
        "slot_code": session.slot.slot_code if session else "Lỗi",
        "passcode": display_passcode,
        "entry_time": session.entry_time.strftime("%H:%M %d/%m") if session else "",
        "expire_at": session.expire_at.strftime("%H:%M %d/%m") if session else "",
        "verify_url": verify_link
    })

@router.get("/verify-page/{session_id}")
def view_verify_page(request: Request, session_id: str):
    return templates.TemplateResponse("verify.html", {
        "request": request,
        "session_id": session_id
    })

@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):

    active_count = db.query(models.ParkingTicketSession).filter(
        models.ParkingTicketSession.status == models.SessionStatus.ACTIVE
    ).count()

    total_count = db.query(models.ParkingTicketSession).count()
    
    empty_slots = db.query(models.ParkingSlot).filter(
        models.ParkingSlot.status == models.SlotStatus.AVAILABLE
    ).count()
    
    recent = db.query(models.ParkingTicketSession).order_by(
        models.ParkingTicketSession.entry_time.desc()
    ).limit(10).all()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "total_active": active_count,
        "total_tickets": total_count,
        "available_slots": empty_slots,
        "recent_tickets": recent
    })