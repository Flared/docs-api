import dataclasses

from lintlify import openapi


@dataclasses.dataclass
class LintContext:
    openapi_files: list[openapi.OpenApiFile]
