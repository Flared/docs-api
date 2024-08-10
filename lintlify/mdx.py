import dataclasses
import typing as t

import frontmatter


@dataclasses.dataclass
class MdxFile:
    fullpath: str
    post: frontmatter.Post

    @classmethod
    def from_filepath(cls, filepath: str) -> t.Self:
        with open(filepath, "r", encoding="utf-8") as f:
            post: frontmatter.Post = frontmatter.loads(f.read())

        return cls(
            fullpath=filepath,
            post=post,
        )

    def save(self) -> None:
        raise NotImplementedError("oh no")
