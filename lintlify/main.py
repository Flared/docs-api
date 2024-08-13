#!/usr/bin/env python3

import glob
import os.path

from lintlify import openapi
from lintlify.context import LintContext
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


def main() -> None:
    docs_dir: str = get_docs_dir()

    # Create the linting context
    lint_context: LintContext = LintContext(
        openapi_files=openapi.get_all_openapi_files(
            docs_dir=docs_dir,
        ),
        mdx_files=get_all_mdx_filenames(
            docs_dir=docs_dir,
        ),
    )

    print("Linting frontmatter...")
    lint_all_frontmatter(
        lint_context=lint_context,
    )

    print("Linting code blocks...")
    lint_all_code_blocks(
        lint_context=lint_context,
    )


if __name__ == "__main__":
    main()
