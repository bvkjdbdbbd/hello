from pydantic import BaseModel
from datetime import datetime

class TicketCreate(BaseModel):
    slot_id: int
    gate_id: int

class TicketResponse(BaseModel):
    session_id: str
    slot_code: str
    passcode: str
    qr_hash: str
    expire_at: datetime
    
    class Config:
        from_attributes = True 

class TicketVerify(BaseModel):
    passcode: str

class TicketVerifyResponse(BaseModel):
    success: bool
    message: str = None
    error: str = None
    session_id: str = None
    exit_time: datetime = None