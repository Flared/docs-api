#!/usr/bin/env python3

import glob
import itertools
import os.path
import sys

from lintlify import openapi
from lintlify.context import LintContext
from lintlify.error import LintError
from lintlify.linters.code_blocks import lint_all_code_blocks
from lintlify.linters.frontmatter import lint_all_frontmatter


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
) -> list[str]:
    return glob.glob(
        os.path.join(
            docs_dir,
            "**",
            "*.mdx",
        ),
        recursive=True,
    )


def print_error(error: LintError) -> None:
    print("==============")
    print(f"ERROR: {error.filename}")
    print(error.message)


def main() -> None:
    docs_dir: str = get_docs_dir()

    lint_context: LintContext = LintContext(
        repository_root=get_repo_dir(),
        openapi_files=openapi.get_all_openapi_files(
            docs_dir=docs_dir,
        ),
        mdx_files=get_all_mdx_filenames(
            docs_dir=docs_dir,
        ),
    )

    has_error: bool = False

    for error in itertools.chain(
        lint_all_frontmatter(
            lint_context=lint_context,
        ),
        lint_all_code_blocks(
            lint_context=lint_context,
        ),
    ):
        has_error = True
        print_error(error)

    if has_error:
        sys.exit(1)


if __name__ == "__main__":
    main()
