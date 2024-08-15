import dataclasses
import re
import subprocess

from lintlify.context import LintContext
from lintlify.error import LintError

import typing as t


@dataclasses.dataclass
class _ExtractedMarkdownBlock:
    header: str
    body: str


def _extract_md_blocks(*, text: str) -> list[_ExtractedMarkdownBlock]:
    pattern: str = r"""```(?P<header>[^\n]*)(?P<body>.*?)```"""
    matches: list[_ExtractedMarkdownBlock] = []
    for match in re.finditer(pattern, text, re.DOTALL):
        matches.append(
            _ExtractedMarkdownBlock(
                header=match.group("header"),
                body=match.group("body"),
            )
        )
    return matches


def _extract_code(
    *,
    filename: str,
    language: str,
) -> list[_ExtractedMarkdownBlock]:
    expected_prefix = f"""```{language}"""

    with open(filename, "r", encoding="utf-8") as f:
        mdx_contents: str = f.read()

    # Don't bother calling codedown
    # if we can't spot the prefix in the file.
    if expected_prefix not in mdx_contents:
        return []

    extracted_code_blocks: list[_ExtractedMarkdownBlock] = _extract_md_blocks(
        text=mdx_contents,
    )
    extracted_code_blocks = [
        code_block
        for code_block in extracted_code_blocks
        if code_block.header.lower().startswith(language.lower())
    ]

    return extracted_code_blocks


def _lint_mdx_file_code_blocks(
    *,
    lint_context: LintContext,
    filename: str,
) -> t.Iterator[LintError]:
    python_blocks: list[_ExtractedMarkdownBlock] = _extract_code(
        filename=filename,
        language="python",
    )

    for python_block in python_blocks:
        # Run mypy
        try:
            subprocess.check_output(
                args=[
                    lint_context.mypy_path,
                    "/dev/stdin",
                ],
                input=python_block.body.encode("utf-8"),
            )
        except subprocess.CalledProcessError as ex:
            yield LintError(
                filename=filename,
                message=ex.stdout.decode(),
            )

        # Run ruff
        try:
            subprocess.check_output(
                args=[
                    lint_context.ruff_path,
                    "check",
                    "--stdin-filename",
                    filename,
                ],
                input=python_block.body.encode("utf-8"),
            )
        except subprocess.CalledProcessError as ex:
            yield LintError(
                filename=filename,
                message=ex.stdout.decode(),
            )


def lint_all_code_blocks(
    *,
    lint_context: LintContext,
) -> t.Iterator[LintError]:
    print("Linting code blocks...")
    for mdx_file in lint_context.mdx_files:
        yield from _lint_mdx_file_code_blocks(
            lint_context=lint_context,
            filename=mdx_file,
        )
