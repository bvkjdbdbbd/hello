# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Khóa bí mật dùng để mã hóa/giải mã (chống giả mạo token)
    SECRET_KEY: str 

    # URL kết nối cơ sở dữ liệu (sẽ được đọc từ .env).
    DATABASE_URL: str

    # Số lần đăng nhập thất bại tối đa
    MAX_FAIL_AUTH: int = 5 

    # Cấu hình PydanticSettings để đọc biến từ file .env
    model_config = SettingsConfigDict(env_file='.env')

# Tạo một instance của Settings để có thể import và sử dụng trong toàn bộ dự án.
settings = Settings()