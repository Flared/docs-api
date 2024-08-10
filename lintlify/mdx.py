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

    def set_property(
        self,
        *,
        name: str,
        value: str,
    ) -> None:
        self.post.metadata[name] = value

    def save(self) -> None:
        with open(self.fullpath, "w", encoding="utf-8") as f:
            f.write(
                frontmatter.dumps(
                    post=self.post,
                )
            )
