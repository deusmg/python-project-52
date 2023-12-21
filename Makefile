PORT ?= 10000


install:
	poetry install

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi:application

shell:
	poetry run python manage.py shell

migrate:
	poetry run python manage.py makemigrations && poetry run python manage.py migrate

lint:
	poetry run flake8 task_manager

