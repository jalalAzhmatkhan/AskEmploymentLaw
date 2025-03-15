@echo off
cls  REM Clears the screen
echo ==========================================================
echo ^|                   Ask Employment Law                   ^|
echo ==========================================================
title Ask Employment Law - Setting up environment
echo Activating Python environment...
call .\venv\Scripts\activate.bat
echo "Adding current repository to Python path..."
setlocal enabledelayedexpansion
$env:PYTHONPATH = $PWD
set PYTHONPATH=%CD%
echo "Python path: %PYTHONPATH%"

echo ==========================================================
echo "Clearing old folders..."
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d
cls

echo ==========================================================
echo ^|                   Ask Employment Law                   ^|
echo ==========================================================
title Ask Employment Law - Checking environment connections
echo "Checking DB Connection..."
python .\core\db_prestart.py
alembic upgrade head

echo "Checking RabbitMQ Connection..."
python .\core\rabbitmq_prestart.py

echo "Initializing data..."
python .\services\init_db_data_service.py
cls

echo ==========================================================
echo ^|                   Ask Employment Law                   ^|
echo ==========================================================
title Ask Employment Law - Run Unit Tests
echo "Running unit tests..."
pytest . --disable-pytest-warnings

echo "Running backend server..."
cls
:: Enable Ctrl+C to immediately terminate the script
title Ask Employment Law - Running
echo ===========================================================
echo ^|                   Ask Employment Law                   ^|
echo ===========================================================
echo Press Ctrl+C to terminate at any time...
echo

uvicorn --reload --host 0.0.0.0 --port 8081 --log-level info main:main_app --access-log --reload-dir .

:: If the script is terminated, force exit
goto :eof
