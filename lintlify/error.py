import dataclasses


@dataclasses.dataclass
class LintError:
    filename: str
    message: str
