install:
	poetry install

check:
	poetry run flake8 find_subscriptions/
	poetry run mypy find_subscriptions/
	poetry run pytest tests/
