from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    """Kiểm tra xem trang chủ có hoạt động không"""
    response = client.get("/")
    assert response.status_code == 200
    assert "SMART PARKING" in response.text 