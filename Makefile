install:
	poetry install

check:
	poetry run flake8 scanner/
	poetry run mypy scanner/
	poetry run pytest tests/
