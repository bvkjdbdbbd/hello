from app.db.database import SessionLocal
from app.db import models
from datetime import datetime

def seed_database():
    db = SessionLocal()
    
    try:
        db.query(models.ParkingTicketSession).delete()
        db.query(models.ParkingSlot).delete()
        db.query(models.Gate).delete()
        db.commit()
        print("✓ Xóa dữ liệu cũ")
        
        gate1 = models.Gate(name="Gate A", id=1)
        gate2 = models.Gate(name="Gate B", id=2)
        db.add_all([gate1, gate2])
        db.commit()
        print("✓ Thêm 2 cổng (Gate A, Gate B)")

        slots = []
        for i in range(1, 11):
            slot = models.ParkingSlot(
                slot_code=f"A-{i:02d}",
                status=models.SlotStatus.AVAILABLE,
                gate_id=1
            )
            slots.append(slot)

        for i in range(1, 11):
            slot = models.ParkingSlot(
                slot_code=f"B-{i:02d}",
                status=models.SlotStatus.AVAILABLE,
                gate_id=2
            )
            slots.append(slot)
        
        db.add_all(slots)
        db.commit()
        print("✓ Thêm 20 chỗ đỗ xe (10 cho Gate A, 10 cho Gate B)")
        
        print("\n✅ Seed dữ liệu thành công!")
        
        gate_count = db.query(models.Gate).count()
        slot_count = db.query(models.ParkingSlot).count()
        print(f"   Gates: {gate_count}")
        print(f"   Slots: {slot_count}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Lỗi: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
