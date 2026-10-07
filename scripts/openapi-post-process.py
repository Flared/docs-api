#!/usr/bin/env python3

import json
import sys

from typing import Any


def find_schema_refs(obj: Any) -> set[str]:
    refs: set[str] = set()

    if isinstance(obj, dict):
        ref = obj.get("$ref")
        if isinstance(ref, str) and ref.startswith("#/components/schemas/"):
            refs.add(ref.removeprefix("#/components/schemas/"))
        for value in obj.values():
            refs |= find_schema_refs(value)
    elif isinstance(obj, list):
        for item in obj:
            refs |= find_schema_refs(item)

    return refs


def remove_unused_schemas(openapi_schema: dict) -> None:
    schemas = openapi_schema.get("components", {}).get("schemas", {})
    if not schemas:
        return

    used = find_schema_refs(openapi_schema["paths"])

    # Schemas can reference other schemas, so keep expanding until no new
    # schema names are discovered.
    frontier = used
    while frontier:
        frontier = (
            set().union(
                *(
                    find_schema_refs(schemas[name])
                    for name in frontier
                    if name in schemas
                )
            )
            - used
        )
        used |= frontier

    for name in list(schemas.keys()):
        if name not in used:
            del schemas[name]


def main() -> None:
    if len(sys.argv) != 2:
        raise Exception("Please pass only one path as the argument")

    path = sys.argv[1]

    with open(path, "r") as f:
        openapi_schema = json.loads(f.read())

    remove_unused_schemas(openapi_schema)

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
        }
    }

    openapi_schema["security"] = [{"BearerAuth": []}]

    with open(path, "w", encoding="utf-8") as f:
        f.write(
            json.dumps(
                openapi_schema,
                indent=4,
            )
        )


if __name__ == "__main__":
    main()
