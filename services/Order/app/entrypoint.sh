
echo "Running Alembic migrations ....."
alembic upgrade head

echo " Starting Gunicorn server..."
exec gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
