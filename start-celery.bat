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

echo "Running backend server..."
cls
:: Enable Ctrl+C to immediately terminate the script
title Ask Employment Law - Running
echo ===========================================================
echo ^|                   Ask Employment Law                   ^|
echo ===========================================================
echo Press Ctrl+C to terminate at any time...
echo

celery -A celery_app worker -P gevent --loglevel=info --pool=solo --concurrency=5 --max-tasks-per-child=5
