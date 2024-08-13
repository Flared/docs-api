import dataclasses
import os

from lintlify import openapi


@dataclasses.dataclass
class LintContext:
    openapi_files: list[openapi.OpenApiFile]
    mdx_files: list[str]
    repository_root: str

    @property
    def mypy_path(self) -> str:
        return os.path.join(
            self.repository_root,
            "venv",
            "bin",
            "mypy",
        )
