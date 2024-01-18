PORT ?= 8000


install:
	poetry install

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

migrate:
	poetry run python manage.py makemigrations && poetry run python manage.py migrate

compile:
	django-admin compilemessages

test:
	poetry run python3 manage.py test

lint:
	poetry run flake8 task_manager

test-coverage:
	poetry run coverage run --source='.' manage.py test
	poetry run coverage report
	poetry run coverage xml
