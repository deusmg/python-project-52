PORT ?= 8000


install:
	poetry install

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

migrate:
	poetry run python manage.py makemigrations && poetry run python manage.py migrate

