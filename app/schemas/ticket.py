# app/schemas/ticket.py
from pydantic import BaseModel
from datetime import datetime

# --- Schema cho việc TẠO (nội bộ) ---
class TicketCreate(BaseModel):
    slot_id: int
    gate_id: int

# --- Schema cho việc TRẢ VỀ (CÁI BỊ LỖI ĐANG TÌM) ---
class TicketResponse(BaseModel):
    session_id: str
    slot_code: str
    passcode: str
    qr_hash: str
    expire_at: datetime
    
    class Config:
        from_attributes = True # Cho phép đọc từ model DB

# --- Schema cho việc XÁC THỰC ---
class TicketVerify(BaseModel):
    passcode: str

# --- Schema cho Response Verify ---
class TicketVerifyResponse(BaseModel):
    success: bool
    message: str = None
    error: str = None
    session_id: str = None
    exit_time: datetime = None