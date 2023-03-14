web: gunicorn app_backend.wsgi
make_migration: python manage.py makemigrations
migrate: python manage.py migrate
celery: celery --app=app_backend worker -l debug 
celery_beat: celery --app=app_backend beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler