# Flare API docs

This repository contains the source of https://api.docs.flare.io.

## Dev Commands

- `make run` will start the docs.
- `make lint` will find errors.
- `make format` will format python code.
- `make api-generate-all` will generate new OpenAPI files and endpoint pages.


## Dependencies

**General**

- `python`: This repository contains a `.python-version` file for [pyenv](https://github.com/pyenv/pyenv). Use it with `pyenv local`.
- `node`: This repository contains a `.nvmrc` file for [nvm](https://github.com/nvm-sh/nvm). Use it with `nvm use`.
- `uv`: https://docs.astral.sh/uv/

**openapi-generator**

You will need `openapi-generator` in order to generate the OpenAPI files.

On macOS, install with:

    brew install openapi-generator

For Linux, see: https://openapi-generator.tech/docs/installation/

## Deploying

Just push to this repository.
