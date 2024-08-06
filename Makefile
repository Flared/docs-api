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
