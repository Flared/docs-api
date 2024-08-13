import dataclasses

from lintlify import mdx
from lintlify.context import LintContext

import typing as t


@dataclasses.dataclass
class _FrontmatterOpenapi:
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

    def to_str(self) -> str:
        return " ".join(
            [
                self.file or "",
                self.method,
                self.path,
            ]
        ).strip()


def _lint_frontmatter_file_openapi(
    *,
    lint_context: LintContext,
    mdx_file: mdx.MdxFile,
) -> None:
    property = _FrontmatterOpenapi.from_raw(
        mdx_file.post.metadata["openapi"],
    )

    for reference_file in lint_context.openapi_files:
        if property.file and property.file != reference_file.frontmatter_name:
            continue

        if property.path in reference_file.paths:
            if not property.file:
                mdx_file.set_property(
                    name="openapi",
                    value=_FrontmatterOpenapi(
                        file=reference_file.frontmatter_name,
                        method=property.method,
                        path=property.path,
                    ).to_str(),
                )
                mdx_file.save()

            break
    else:
        raise Exception(
            f"Error in file={mdx_file.fullpath}, could not find OpenAPI path {property.path}",
        )


def _lint_frontmatter_file(
    *,
    lint_context: LintContext,
    filename: str,
) -> None:
    mdx_file = mdx.MdxFile.from_filepath(filename)

    if "openapi" in mdx_file.post.metadata:
        _lint_frontmatter_file_openapi(
            lint_context=lint_context,
            mdx_file=mdx_file,
        )


def lint_all_frontmatter(
    *,
    lint_context: LintContext,
) -> None:
    for mdx_filename in lint_context.mdx_files:
        _lint_frontmatter_file(
            filename=mdx_filename,
            lint_context=lint_context,
        )
