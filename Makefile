.PHONY: api-v4-generate-pages
api-v4-generate-pages:
	cd api-reference/v4/endpoints && npx @mintlify/scraping@latest openapi-file ../openapi-example.json

.PHONY: api-v3-update-openapi
api-v3-update-openapi:
	#curl --location https://api.flare.io/firework/docs/firework/v3/swagger.json -o api-reference/v3/swagger.json
#	openapi-generator generate -g openapi -i api-reference/v3/swagger.json -o api-reference/v3
#	cd api-reference/v3 && npx swagger2openapi@7.0.8 swagger.json --outfile openapi.json
	cd api-reference/v3 && npx @mintlify/scraping@latest openapi-file openapi.json
