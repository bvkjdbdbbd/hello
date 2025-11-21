# app/db/database.py (CODE GỐC ĐÃ KHÔI PHỤC)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings # Lấy cấu hình DB URL

# Tạo Engine (Trình kết nối DB)
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)

# Tạo SessionLocal (Phiên làm việc với DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency Injection: Hàm này cấp một session DB cho mỗi request API
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()