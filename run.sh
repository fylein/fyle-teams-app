python manage.py migrate
uvicorn fyle_teams_service.asgi:application --reload --host=0.0.0.0 --port=8000
# gunicorn -c gunicorn_config.py fyle_teams_service.asgi -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000