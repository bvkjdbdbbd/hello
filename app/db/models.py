from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base 
import enum

class SlotStatus(enum.Enum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    MAINTENANCE = "MAINTENANCE"

class SessionStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    EXITED = "EXITED"
    LOCKED = "LOCKED"

class Gate(Base):
    __tablename__ = "gates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    
    slots = relationship("ParkingSlot", back_populates="gate")
    sessions = relationship("ParkingTicketSession", back_populates="gate")

    def __str__(self):
        return self.name

class ParkingSlot(Base):
    __tablename__ = "parking_slots"
    id = Column(Integer, primary_key=True, index=True)
    slot_code = Column(String(10), unique=True, index=True, nullable=False)
    status = Column(Enum(SlotStatus), default=SlotStatus.AVAILABLE, nullable=False)
    
    gate_id = Column(Integer, ForeignKey("gates.id"), nullable=True) 
    
    gate = relationship("Gate", back_populates="slots")
    sessions = relationship("ParkingTicketSession", back_populates="slot")

    def __str__(self):
        return f"{self.slot_code} ({self.status.value})"

class ParkingTicketSession(Base):
    __tablename__ = "parking_ticket_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    session_id = Column(String(20), unique=True, index=True, nullable=False)
    passcode_hash = Column(String(255), nullable=False)
    qr_hash = Column(String(10), nullable=False)
    status = Column(Enum(SessionStatus), default=SessionStatus.ACTIVE, nullable=False)
    fail_auth_count = Column(Integer, default=0, nullable=False)
    entry_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    exit_time = Column(DateTime, nullable=True)
    expire_at = Column(DateTime, nullable=False)

    slot_id = Column(Integer, ForeignKey("parking_slots.id"), nullable=False)
    gate_id = Column(Integer, ForeignKey("gates.id"), nullable=False)
    
    slot = relationship("ParkingSlot", back_populates="sessions")
    gate = relationship("Gate", back_populates="sessions")

    def __str__(self):
        return f"Vé: {self.session_id}"