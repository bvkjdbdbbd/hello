@echo off
echo --- DANG CAI DAT MOI TRUONG CHO DU AN ---

echo 1. Dang tao moi truong ao (venv)...
python -m venv venv

echo 2. Dang kich hoat venv...
call .\venv\Scripts\activate

echo 3. Dang cai dat thu vien tu requirements.txt...
pip install -r requirements.txt

echo.
echo --- TAO FILE .ENV TU DONG ---
echo SECRET_KEY=SUPER_SECRET_KEY_123 > .env
echo DATABASE_URL=sqlite:///./sql_app.db >> .env
echo MAX_FAIL_AUTH=5 >> .env

echo.
echo --- CAI DAT THANH CONG! ---
echo Bay gio ban co the chay file 'run_server.bat' de khoi dong.
pause