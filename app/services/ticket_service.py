# app/services/ticket_service.py

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
import string
import hmac
import hashlib
import bcrypt

from app.crud import parking as crud_parking
from app.core.config import settings
from app.db import models

# --- CÁC HÀM TIỆN ÍCH ---
def _generate_passcode(length: int = 6) -> str:
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def _generate_qr_hash(session_id: str) -> str:
    secret = settings.SECRET_KEY.encode()
    message = session_id.encode()
    return hmac.new(secret, message, hashlib.sha256).hexdigest()[:10]

def _hash_passcode(passcode: str) -> str:
    pwd_bytes = passcode.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def verify_passcode(plain_passcode: str, hashed_passcode: str) -> bool:
    try:
        return bcrypt.checkpw(plain_passcode.encode('utf-8'), hashed_passcode.encode('utf-8'))
    except:
        return False

# --- HÀM TẠO VÉ (CÁI CẬU ĐANG THIẾU) ---
def create_ticket(db: Session, gate_id: int):
    # 1. Tìm slot trống (Gọi CRUD)
    slot = crud_parking.get_available_slot(db, gate_id)
    if not slot:
        return None
    
    # 2. Tính toán mã
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    session_id = f"S-{timestamp}-{slot.id}"
    passcode = _generate_passcode()
    passcode_hash = _hash_passcode(passcode)
    qr_hash = _generate_qr_hash(session_id)
    expire_at = datetime.utcnow() + timedelta(hours=6)

    # 3. Chuẩn bị dữ liệu để lưu
    session_data = {
        "session_id": session_id,
        "passcode_hash": passcode_hash,
        "qr_hash": qr_hash,
        "expire_at": expire_at,
        "slot_id": slot.id,
        "gate_id": gate_id
    }

    # 4. Gọi CRUD để lưu
    db_session = crud_parking.create_db_session(db, session_data, slot)
    
    # Gắn passcode gốc để trả về
    db_session.passcode_plain_for_response = passcode
    return db_session

# --- HÀM LẤY XE ---
def process_exit(db: Session, session_id: str, passcode: str):
    session = crud_parking.get_session_by_id(db, session_id)
    if not session:
        return {"success": False, "error": "Session not found"}
    
    if session.status == models.SessionStatus.LOCKED:
        return {"success": False, "error": "LOCKED"}
    if session.status == models.SessionStatus.EXITED:
        return {"success": False, "error": "Already exited"}
    
    if not verify_passcode(passcode, session.passcode_hash):
        crud_parking.increment_fail_count(db, session)
        return {"success": False, "error": "Invalid passcode"}
    
    crud_parking.update_session_exit(db, session)
    return {"success": True, "message": "Exit successful"}