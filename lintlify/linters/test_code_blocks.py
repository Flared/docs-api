from lintlify.linters.code_blocks import _extract_md_blocks
from lintlify.linters.code_blocks import _ExtractedMarkdownBlock


def test_extract_md_blocks() -> None:
    assert _extract_md_blocks(
        text="""

```python
print("hello")
```

```python HEY
import os
```

"""
    ) == [
        _ExtractedMarkdownBlock(
            header="python",
            body="""
print("hello")
""",
        ),
        _ExtractedMarkdownBlock(
            header="python HEY",
            body="""
import os
""",
        ),
    ]
