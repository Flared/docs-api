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
	mintlify broken-links

.PHONY: lint
lint: broken-links venv
	venv/bin/python scripts/lintlify.py

venv: requirements.txt
	rm -rf venv
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt


.PHONY: clean
clean:
	rm -rf venv
