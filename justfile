set dotenv-load

start:
    python manage.py runserver

migrations:
    python manage.py makemigrations

migrate:
    python manage.py migrate

super:
    python manage.py createsuperuser

shell:
    python manage.py shell