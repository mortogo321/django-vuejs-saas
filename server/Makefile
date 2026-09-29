.PHONY: lint test run migrate

lint:
	ruff check .
	ruff format --check .

test:
	pytest -q

run:
	python manage.py runserver 0.0.0.0:8000

migrate:
	python manage.py migrate
