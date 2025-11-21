# app/db/base.py
from sqlalchemy.orm import DeclarativeBase

# Đây là "nền móng" cho tất cả các Model (bảng) trong database.
# Mọi Model khác sẽ kế thừa từ lớp Base này.
class Base(DeclarativeBase):
    pass