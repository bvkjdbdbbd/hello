# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

# Tạo một client giả lập để test API
client = TestClient(app)

def test_read_root():
    """Kiểm tra xem trang chủ có hoạt động không"""
    response = client.get("/")
    assert response.status_code == 200
    # Kiểm tra xem trong nội dung trả về có chữ "SMART PARKING" không
    # (Vì chúng ta đang dùng HTML template)
    assert "SMART PARKING" in response.text 