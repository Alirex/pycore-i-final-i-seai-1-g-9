from typing import NewType

from prompt_toolkit import HTML

RichFormattedText = NewType("RichFormattedText", str)
"""Text with Rich formatting.

Ensure that the text is formatted correctly.

Use `rich.markup.escape` to escape special characters.
https://rich.readthedocs.io/en/latest/markup.html#escaping
"""

type PromptToolkitFormattedText = HTML | str
