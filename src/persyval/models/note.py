import enum
import uuid
from functools import cache
from typing import TYPE_CHECKING, Annotated, Final, NewType

from prompt_toolkit import HTML
from pydantic import BaseModel, ConfigDict, Field

from persyval.services.model_meta.field_meta import FieldItemMetaConfig, FieldsMetaConfig, FilterMode
from persyval.services.model_meta.model_meta_info import ModelMetaInfo

if TYPE_CHECKING:
    from persyval.services.console.types import PromptToolkitFormattedText


TRIM_CONTENT_PREVIEW: Final[int] = 40
LONG_PLACEHOLDER: Final[str] = "..."

NoteUid = NewType("NoteUid", uuid.UUID)


class AllowedKeysToFilterForNote(enum.StrEnum):
    TITLE = "title"
    CONTENT = "content"
    TAG = "tag"


ALLOWED_KEYS_TO_FILTER_FOR_NOTE: Final[set[str]] = set(AllowedKeysToFilterForNote)


class Note(BaseModel):
    uid: NoteUid = Field(default_factory=lambda: NoteUid(uuid.uuid7()))
    title: Annotated[
        str | None,
        Field(description="The optional title for the note."),
    ] = None
    content: Annotated[
        str,
        Field(description="The main content of the note.", min_length=1),
    ]

    tags: Annotated[
        list[str] | None,
        Field(
            default_factory=list,
            description="List of note tags.",
        ),
    ]

    model_config = ConfigDict(
        validate_assignment=True,
    )

    def get_prompt_toolkit_output(self) -> PromptToolkitFormattedText:
        single_line_content = self.content.replace("\n", " ")

        is_real_title = self.title is not None

        if is_real_title:
            display_title = self.title or ""
        elif len(single_line_content) > TRIM_CONTENT_PREVIEW:
            preview_size = TRIM_CONTENT_PREVIEW - len(LONG_PLACEHOLDER)
            display_title = f"{single_line_content[:preview_size]}{LONG_PLACEHOLDER}"
        else:
            display_title = single_line_content

        title_tag = "b" if is_real_title else "i"
        text = f"<{title_tag}>{display_title}</{title_tag}>"

        text += f"\n<i>{self.uid}</i>"

        return HTML(text)

    @classmethod
    @cache
    def get_meta_info(cls) -> ModelMetaInfo:
        return ModelMetaInfo.from_class(
            cls,
            fields_meta_config=FieldsMetaConfig(
                fields=[
                    FieldItemMetaConfig(
                        name="uid",
                        description="The unique identifier.",
                        filter_mode=FilterMode.EXACT,
                        is_groupable=False,
                        parse_func=lambda x: NoteUid(uuid.UUID(str(x))),  # pyright: ignore[reportUnknownArgumentType, reportUnknownLambdaType]
                    ),
                    FieldItemMetaConfig(
                        name="title",
                        description="The title.",
                        is_groupable=False,
                    ),
                    FieldItemMetaConfig(
                        name="content",
                        description="The main content.",
                        is_groupable=False,
                    ),
                    FieldItemMetaConfig(
                        name="tags",
                        aliases=["tag"],
                        description="List of tags associated with the item.",
                        is_list_based=True,
                    ),
                ],
            ),
        )
