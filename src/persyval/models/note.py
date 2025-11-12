import uuid
from typing import TYPE_CHECKING, Annotated, Final, NewType

from prompt_toolkit import HTML
from pydantic import BaseModel, ConfigDict, Field

from persyval.models.contact import ContactUid

if TYPE_CHECKING:
    from persyval.services.console.types import PromptToolkitFormattedText


TRIM_CONTENT_PREVIEW: Final[int] = 40
LONG_PLACEHOLDER: Final[str] = "..."

NoteUid = NewType("NoteUid", uuid.UUID)


class Note(BaseModel):
    uid: NoteUid = Field(default_factory=lambda: NoteUid(uuid.uuid7()))
    contact_uid: ContactUid
    title: Annotated[
        str | None,
        Field(description="The optional title for the note."),
    ] = None
    content: Annotated[
        str,
        Field(description="The main content of the note.", min_length=1),
    ]

    model_config = ConfigDict(
        validate_assignment=True,
    )

    def get_prompt_toolkit_output(self) -> PromptToolkitFormattedText:
        display_title: str
        is_real_title: bool = False

        if self.title:
            display_title = self.title
            is_real_title = True
        elif len(self.content) > TRIM_CONTENT_PREVIEW:
            size = TRIM_CONTENT_PREVIEW - len(LONG_PLACEHOLDER)
            display_title = f"{self.content.replace(chr(10), ' ')[:size]}{LONG_PLACEHOLDER}"
        else:
            display_title = self.content.replace(chr(10), " ")

        text: str
        text = f"<b>{display_title}</b>" if is_real_title else f"<i>{display_title}</i>"

        text += f"  (<i>{self.uid}</i>)"

        return HTML(text)
