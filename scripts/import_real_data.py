"""
Import real Gate and ParkingSlot data from a CSV file into the app's database.
Usage (PowerShell):
  $env:PYTHONPATH = "d:\parking_qr"; python scripts\import_real_data.py data\real_slots.csv

CSV format: gate_name,slot_code

This script is idempotent for Gates and Slots (will not duplicate existing gate names or slot_codes).
"""
import sys
import csv
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db.database import SessionLocal
from app.db import models


def import_csv(csv_path: str):
    db = SessionLocal()
    path = Path(csv_path)
    if not path.exists():
        print(f"CSV file not found: {csv_path}")
        return

    created_gates = 0
    created_slots = 0

    try:
        with path.open('r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                gate_name = row.get('gate_name')
                slot_code = row.get('slot_code')
                if not gate_name or not slot_code:
                    print(f"Skipping invalid row: {row}")
                    continue

                gate = db.query(models.Gate).filter(models.Gate.name == gate_name).first()
                if not gate:
                    gate = models.Gate(name=gate_name)
                    db.add(gate)
                    db.commit()
                    db.refresh(gate)
                    created_gates += 1

                existing = db.query(models.ParkingSlot).filter(models.ParkingSlot.slot_code == slot_code).first()
                if existing:
                    if existing.gate_id != gate.id:
                        existing.gate_id = gate.id
                        db.add(existing)
                        db.commit()
                        print(f"Updated slot {slot_code} -> gate {gate_name}")
                    else:
                        pass
                else:
                    slot = models.ParkingSlot(slot_code=slot_code, status=models.SlotStatus.AVAILABLE, gate_id=gate.id)
                    db.add(slot)
                    db.commit()
                    created_slots += 1

        print(f"Import finished. Gates created: {created_gates}, Slots created: {created_slots}")
    except Exception as e:
        db.rollback()
        print(f"Error during import: {e}")
    finally:
        db.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scripts/import_real_data.py path/to/real_slots.csv")
    else:
        import_csv(sys.argv[1])
