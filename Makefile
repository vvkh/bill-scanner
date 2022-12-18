install:
	poetry install

check:
	poetry run flake8 subscriptions/
	poetry run mypy subscriptions/
	poetry run pytest tests/
