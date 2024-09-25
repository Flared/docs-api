#!/usr/bin/env python3

import os
import sys

from enum import StrEnum
from flareio import FlareApiClient

from typing import assert_never


class FireworkApiVersion(StrEnum):
    V2 = "v2"
    V3 = "v3"
    V4 = "v4"


def get_apispec_url(version: FireworkApiVersion) -> str:
    match version:
        case FireworkApiVersion.V2:
            return "https://api.flare.io/firework/docs/firework/v2/swagger.json"
        case FireworkApiVersion.V3:
            return "https://api.flare.io/firework/docs/firework/v3/swagger.json"
        case FireworkApiVersion.V4:
            return "https://api.flare.io/firework/firework/v4/docs/openapi.json"
        case never:
            return assert_never(never)


def main() -> None:
    if len(sys.argv) != 2:
        raise Exception(
            "This script only takes one argument: the api version (v2, v3 or v4)."
        )

    try:
        version = FireworkApiVersion(sys.argv[1])
    except ValueError:
        raise Exception(
            f"Provided api version is invalid: '{sys.argv[1]}'. Valid versions are v2, v3 and v4."
        )

    url: str = get_apispec_url(version)

    print(FlareApiClient(api_key=os.environ["FLARE_API_KEY"]).get(url).text)


if __name__ == "__main__":
    main()
