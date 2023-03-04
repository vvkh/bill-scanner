install:
	poetry install

check:
	poetry run ruff ./
	poetry run pyright ./
	poetry run pytest tests/
