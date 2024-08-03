#!/usr/bin/env python3

import json
import sys

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

    with open(path, "w", encoding="utf-8") as f:
        f.write(
            json.dumps(
                openapi_schema,
                indent=4,
            )
        )

if __name__ == "__main__":
    main()
