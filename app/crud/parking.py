# app/crud/parking.py (PHIÊN BẢN CHUẨN - CHỈ THAO TÁC DB)
from sqlalchemy.orm import Session
from datetime import datetime
from app.db import models

# 1. Tìm slot trống
def get_available_slot(db: Session, gate_id: int):
    return db.query(models.ParkingSlot).filter(
        models.ParkingSlot.status == models.SlotStatus.AVAILABLE,
        (models.ParkingSlot.gate_id == gate_id) | (models.ParkingSlot.gate_id == None)
    ).first()

# 2. Tìm session theo ID
def get_session_by_id(db: Session, session_id: str):
    return db.query(models.ParkingTicketSession).filter(
        models.ParkingTicketSession.session_id == session_id
    ).first()

# 3. LƯU VÉ VÀO DB (Service sẽ gọi hàm này)
def create_db_session(db: Session, session_data: dict, slot: models.ParkingSlot):
    db_session = models.ParkingTicketSession(**session_data)
    slot.status = models.SlotStatus.OCCUPIED
    
    db.add(db_session)
    db.add(slot)
    db.commit()
    db.refresh(db_session)
    return db_session

# 4. Update lỗi
def increment_fail_count(db: Session, session: models.ParkingTicketSession):
    session.fail_auth_count += 1
    if session.fail_auth_count >= 5:
        session.status = models.SessionStatus.LOCKED
    db.commit()

# 5. Update thoát
def update_session_exit(db: Session, session: models.ParkingTicketSession):
    session.status = models.SessionStatus.EXITED
    session.exit_time = datetime.utcnow()
    session.slot.status = models.SlotStatus.AVAILABLE
    db.commit()