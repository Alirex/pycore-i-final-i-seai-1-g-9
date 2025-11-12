from typing import TYPE_CHECKING

from pydantic import BaseModel

from persyval.models.note import Note
from persyval.services.commands.command_meta import ArgMetaConfig, ArgsConfig
from persyval.services.data_actions.note_add import note_add
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_good_message

if TYPE_CHECKING:
    from persyval.services.handlers_base.handler_output import HandlerOutput


class NoteAddIArgs(BaseModel):
    content: str
    title: str | None = None


NOTE_ADD_I_ARGS_CONFIG = ArgsConfig[NoteAddIArgs](
    result_cls=NoteAddIArgs,
    args=[
        ArgMetaConfig(
            name="content",
            required=True,
        ),
        ArgMetaConfig(
            name="title",
            required=False,
        ),
    ],
)


class NoteAddIHandler(
    HandlerBase,
):
    def _handler(self) -> HandlerOutput | None:
        parse_result = NOTE_ADD_I_ARGS_CONFIG.parse(self.args)

        note = Note(
            title=parse_result.title,
            content=parse_result.content,
        )

        note_add(data_storage=self.data_storage, note=note)

        render_good_message(
            self.console,
            "Note added successfully.",
        )

        return None
