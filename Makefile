.PHONY: run
run:
	cd docs && npx mintlify dev

.PHONY: api-generate-openapi
api-generate-openapi:
	./scripts/api-generate-openapi

.PHONY: api-generate-pages
api-generate-pages:
	./scripts/api-generate-pages

.PHONY: api-generate-all
api-generate-all:
	./scripts/api-generate-openapi
	./scripts/api-generate-pages

.PHONY: boken-links
broken-links:
	cd docs && npx mintlify broken-links

.PHONY: lintlify
lintlify: venv
	venv/bin/python -m lintlify.main

.PHONY: lint
lint: broken-links venv mypy lintlify format-check

.PHONY: format
format: venv
	venv/bin/ruff check --fix
	venv/bin/ruff format

.PHONY: format-check
format-check: venv
	venv/bin/ruff format --check

.PHONY: mypy
mypy:
	venv/bin/mypy --strict scripts/*.py
	venv/bin/mypy --strict --ignore-missing-imports -p lintlify

venv: requirements.txt
	rm -rf venv
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt

.PHONY: test
test: venv
	PYTHONPATH=. venv/bin/pytest lintlify -vv

.PHONY: clean
clean:
	rm -rf venv
