start:
	poetry run python manage.py runserver

shell:
	poetry run python manage.py shell

migrate:
	poetry run python manage.py makemigrations && poetry run python manage.py migrate

lint:
	poetry run flake8 task_manager
