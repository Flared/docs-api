#!/usr/bin/env python3

import json
import sys

from copy import copy
from urllib.parse import urlparse

from typing import Any


def set_security(openapi_schema: dict[str, Any]) -> None:
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
        }
    }

    openapi_schema["security"] = [{"BearerAuth": []}]


def put_prefix_into_paths(openapi_schema: dict[str, Any]) -> None:
    url = urlparse(openapi_schema["servers"][0]["url"])
    openapi_schema["servers"][0]["url"] = url._replace(path="").geturl()

    server_path: str = url.path.rstrip("/")
    path: str
    for path in copy(openapi_schema["paths"]):
        new_path = f"{server_path}{path}"
        openapi_schema["paths"][new_path] = openapi_schema["paths"][path]
        del openapi_schema["paths"][path]


def write_schema(openapi_schema: dict[str, Any], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(
            json.dumps(
                openapi_schema,
                indent=4,
            )
        )


def main() -> None:
    if len(sys.argv) != 2:
        raise Exception("Please pass only one path as the argument")

    path = sys.argv[1]

    with open(path, "r") as f:
        openapi_schema: dict[str, Any] = json.loads(f.read())

    set_security(openapi_schema)
    put_prefix_into_paths(openapi_schema)

    write_schema(openapi_schema, path)


if __name__ == "__main__":
    main()
