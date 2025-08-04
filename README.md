# Flare API docs

This repository contains the source of https://api.docs.flare.io.

## Dev Commands

- `make run` will start the docs.
- `make lint` will find errors.
- `make format` will format python code.
- `make api-generate-all` will generate new OpenAPI files and endpoint pages.

Note: you will need `openapi-generator` in order to generate the OpenAPI files.

On macOS, install with:

    brew install openapi-generator

For Linux, see: https://openapi-generator.tech/docs/installation/

## Deploying

Just push to this repository.
