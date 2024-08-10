#!/usr/bin/env python3

import dataclasses
import glob
import os.path
import typing as t

from lintlify import mdx, openapi
from lintlify.context import LintContext


def get_repo_dir() -> str:
    return os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
        )
    )


def get_docs_dir() -> str:
    return os.path.join(
        get_repo_dir(),
        "docs",
    )


def get_all_mdx_filenames(
    *,
    docs_dir: str,
) -> t.Iterator[str]:
    for filename in glob.iglob(
        os.path.join(
            docs_dir,
            "**",
            "*.mdx",
        ),
        recursive=True,
    ):
        yield filename


@dataclasses.dataclass
class FrontmatterOpenapi:
    file: str | None
    method: str
    path: str

    @classmethod
    def from_raw(cls, api_raw: str) -> t.Self:
        api_split: list[str] = api_raw.split(" ")
        if len(api_split) == 3:
            return cls(
                file=api_split[0],
                method=api_split[1],
                path=api_split[2],
            )
        if len(api_split) == 2:
            return cls(
                file=None,
                method=api_split[0],
                path=api_split[1],
            )
        raise Exception(f"Unknown api frontmatter format: {api_raw}")


def lint_frontmatter_file_openapi(
    *,
    lint_context: LintContext,
    mdx_file: mdx.MdxFile,
) -> None:
    openapi_property = FrontmatterOpenapi.from_raw(
        mdx_file.post.metadata["openapi"],
    )

    for openapi_file in lint_context.openapi_files:
        if (
            openapi_property.file
            and openapi_property.file != openapi_file.frontmatter_name
        ):
            continue

        if openapi_property.path in openapi_file.paths:
            if not openapi_property.file:
                # TODO: add the file...
                pass
            break
    else:
        raise Exception(
            f"Error in file={mdx_file.fullpath}, could not find OpenAPI path {openapi_property.path}",
        )


def lint_frontmatter_file(
    *,
    lint_context: LintContext,
    filename: str,
) -> None:
    mdx_file = mdx.MdxFile.from_filepath(filename)

    if "openapi" in mdx_file.post.metadata:
        lint_frontmatter_file_openapi(
            lint_context=lint_context,
            mdx_file=mdx_file,
        )


def lint_all_frontmatter(
    *,
    docs_dir: str,
    lint_context: LintContext,
) -> None:
    for mdx_filename in get_all_mdx_filenames(docs_dir=docs_dir):
        lint_frontmatter_file(
            filename=mdx_filename,
            lint_context=lint_context,
        )


def main() -> None:
    docs_dir: str = get_docs_dir()

    # Find all OpenAPI filenames
    openapi_files = openapi.get_all_openapi_files(
        docs_dir=docs_dir,
    )

    # Create the linting context
    lint_context: LintContext = LintContext(
        openapi_files=openapi_files,
    )

    print("Linting frontmatter...")
    lint_all_frontmatter(
        docs_dir=docs_dir,
        lint_context=lint_context,
    )


if __name__ == "__main__":
    main()
