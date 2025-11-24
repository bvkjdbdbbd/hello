from sqlalchemy.orm import Session
from datetime import datetime
from app.db import models

def get_available_slot(db: Session, gate_id: int):
    return db.query(models.ParkingSlot).filter(
        models.ParkingSlot.status == models.SlotStatus.AVAILABLE,
        (models.ParkingSlot.gate_id == gate_id) | (models.ParkingSlot.gate_id == None)
    ).first()

def get_session_by_id(db: Session, session_id: str):
    return db.query(models.ParkingTicketSession).filter(
        models.ParkingTicketSession.session_id == session_id
    ).first()

def create_db_session(db: Session, session_data: dict, slot: models.ParkingSlot):
    db_session = models.ParkingTicketSession(**session_data)
    slot.status = models.SlotStatus.OCCUPIED
    
    db.add(db_session)
    db.add(slot)
    db.commit()
    db.refresh(db_session)
    return db_session

def increment_fail_count(db: Session, session: models.ParkingTicketSession):
    session.fail_auth_count += 1
    if session.fail_auth_count >= 5:
        session.status = models.SessionStatus.LOCKED
    db.commit()

def update_session_exit(db: Session, session: models.ParkingTicketSession):
    session.status = models.SessionStatus.EXITED
    session.exit_time = datetime.utcnow()
    session.slot.status = models.SlotStatus.AVAILABLE
    db.commit()