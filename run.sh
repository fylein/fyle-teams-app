python manage.py migrate
gunicorn -c gunicorn_config.py fyle_teams_service.asgi -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000