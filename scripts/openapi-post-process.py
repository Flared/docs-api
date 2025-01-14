#!/usr/bin/env python3

import json
import sys

from typing import Any


def filter_search_after_from_me_feed_credentials(
    openapi_schema: dict[str, Any],
) -> dict[str, Any]:
    parameters: list[dict[str, Any]] | None = (
        openapi_schema.get("paths", {})
        .get("/me/feed/credentials", {})
        .get("get", {})
        .get("parameters")
    )

    if parameters:
        openapi_schema["paths"]["/me/feed/credentials"]["get"]["parameters"] = [
            param for param in parameters if param["name"] != "search_after"
        ]

    return openapi_schema


def main() -> None:
    if len(sys.argv) != 2:
        raise Exception("Please pass only one path as the argument")

    path = sys.argv[1]

    with open(path, "r") as f:
        openapi_schema = json.loads(f.read())

    openapi_schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
    }

    openapi_schema = filter_search_after_from_me_feed_credentials(openapi_schema)

    with open(path, "w", encoding="utf-8") as f:
        f.write(
            json.dumps(
                openapi_schema,
                indent=4,
            )
        )


if __name__ == "__main__":
    main()
