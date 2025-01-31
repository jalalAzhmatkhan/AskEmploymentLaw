@echo off
echo "=================================================="
echo "|               Ask Employment Law               |"
echo "=================================================="
echo "Activating Python environment..."
call .\venv\Scripts\activate.bat
echo "Adding current repository to Python path..."
$env:PYTHONPATH = $PWD
echo "Python path: $env:PYTHONPATH"

echo "Checking DB Connection..."
python .\core\db_prestart.py

echo "Checking RabbitMQ Connection..."
python .\core\rabbitmq_prestart.py

echo "Initializing data..."
python .\services\init_db_data_service.py

echo "Running backend server..."
uvicorn --reload --host 0.0.0.0 --port 8081 --log-level info main:main_app --access-log --reload-dir .
