all: ruff

ruff:
	uv run ruff check --fix
	uv run ruff format

check:
	uv run basedpyright .
	