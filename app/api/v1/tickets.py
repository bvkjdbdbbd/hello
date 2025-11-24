from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import ticket as schemas
from app.services import ticket_service 

router = APIRouter(
    prefix="/api/v1",
    tags=["Parking Tickets"]
)

@router.get("/entry/{gate_id}", response_model=schemas.TicketResponse)
def create_ticket_entry(gate_id: int, db: Session = Depends(get_db)):
    db_session = ticket_service.create_ticket(db=db, gate_id=gate_id)
    
    if db_session is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No available parking slots."
        )
        
    return schemas.TicketResponse(
        session_id=db_session.session_id,
        slot_code=db_session.slot.slot_code,
        passcode=db_session.passcode_plain_for_response,
        qr_hash=db_session.qr_hash,
        expire_at=db_session.expire_at
    )

@router.post("/verify/{session_id}")
def verify_ticket_exit(session_id: str, verify_data: schemas.TicketVerify, db: Session = Depends(get_db)):
    result = ticket_service.process_exit(
        db=db, 
        session_id=session_id, 
        passcode=verify_data.passcode
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=result["error"]
        )
    
    return result