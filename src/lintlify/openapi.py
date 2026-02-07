import dataclasses
import glob
import json
import os

import typing as t


def _get_all_openapi_filenames(*, docs_dir: str) -> t.Iterator[str]:
    for filename in glob.iglob(
        os.path.join(
            docs_dir,
            "**",
            "*openapi.json",
        ),
        recursive=True,
    ):
        yield filename


@dataclasses.dataclass
class OpenApiFile:
    fullpath: str
    reference: dict[str, t.Any]

    @property
    def frontmatter_name(self) -> str:
        base_name = os.path.basename(self.fullpath)
        base_name_split = os.path.splitext(base_name)
        return base_name_split[0]

    @property
    def paths(self) -> list[str]:
        return list(self.reference["paths"].keys())


def get_all_openapi_files(*, docs_dir: str) -> list[OpenApiFile]:
    openapi_files = []
    for filename in _get_all_openapi_filenames(
        docs_dir=docs_dir,
    ):
        with open(filename, mode="r", encoding="utf-8") as f:
            reference: dict[str, t.Any] = json.loads(f.read())
        openapi_files.append(
            OpenApiFile(
                fullpath=filename,
                reference=reference,
            )
        )
    return openapi_files
