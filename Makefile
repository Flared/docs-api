.PHONY: openapi-generate
openapi-generate:
	cd api-reference/v4 && npx @mintlify/scraping@latest openapi-file ../openapi-example.json
