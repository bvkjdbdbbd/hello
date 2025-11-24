@echo off
echo --- DANG KICH HOAT MOI TRUONG AO ---
call .\venv\Scripts\activate

echo.
echo --- DIA CHI IP MAY CUA CAU LA: ---
ipconfig | findstr "IPv4"

echo.
echo --- DANG KHOI DONG SERVER... ---
echo Hay dung IP o tren de vao web nhe! (Vi du: http://192.168.x.x:8000/entry-redirect/1)
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause