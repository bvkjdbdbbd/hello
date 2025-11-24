from app.db import models
from app.db.database import SessionLocal, engine

def seed_data():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(models.Gate).count() == 0:
            print("--- DATABASE RỖNG, ĐANG MỒI DỮ LIỆU... ---")
            
            gate1 = models.Gate(name="Cổng A (Vào)")
            gate2 = models.Gate(name="Cổng B (Ra)")
            db.add(gate1)
            db.add(gate2)
            db.commit() 

            for i in range(1, 21):
                slot = models.ParkingSlot(
                    slot_code=f"A-{i:02d}", 
                    status=models.SlotStatus.AVAILABLE,
                    gate_id=gate1.id
                )
                db.add(slot)
        
            db.commit()
            print("--- MỒI DỮ LIỆU THÀNH CÔNG (20 Slots) ---")
        else:
            print("--- Database đã có dữ liệu. ---")
    finally:
        db.close()