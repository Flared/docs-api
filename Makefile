.PHONY: run
run:
	cd docs && npx mintlify dev

.PHONY: api-generate-openapi
api-generate-openapi: venv
	bash -c '\
		source .venv/bin/activate \
		&& ./scripts/api-generate-openapi \
	'

.PHONY: api-generate-pages
api-generate-pages: venv
	bash -c '\
		source .venv/bin/activate \
		&& ./scripts/api-generate-pages \
	'

.PHONY: api-generate-all
api-generate-all: venv
	bash -c '\
		source .venv/bin/activate \
		&& ./scripts/api-generate-openapi \
		&& ./scripts/api-generate-pages \
	'

.PHONY: boken-links
broken-links:
	cd docs && npx mintlify broken-links

.PHONY: lintlify
lintlify: venv
	.venv/bin/python -m lintlify.main

.PHONY: lint
lint: broken-links mypy lintlify format-check

.PHONY: ci
ci: broken-links mypy lintlify format-check test

.PHONY: format
format: venv
	uv run ruff check --fix
	uv run ruff format

.PHONY: format-check
format-check: venv
	uv run ruff format --check

.PHONY: mypy
mypy: venv
	uv run mypy --strict scripts/*.py
	uv run mypy --strict --ignore-missing-imports -p lintlify

.PHONY: venv
venv: .venv

.venv: uv.lock pyproject.toml
	uv sync

.PHONY: test
test: venv
	uv run pytest src -vv

.PHONY: clean
clean:
	rm -rf venv
