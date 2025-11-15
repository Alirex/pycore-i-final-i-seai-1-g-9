import uuid
from typing import TYPE_CHECKING

from persyval.models.note import (
    Note,
    NoteUid,
)
from persyval.services.commands.args_config import ArgMetaConfig, ArgsConfig, ArgType
from persyval.services.data_actions.note_delete import note_delete
from persyval.services.execution_queue.execution_queue import HandlerArgsBase
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_canceled_message, render_good_message

if TYPE_CHECKING:
    from persyval.services.handlers_base.handler_output import HandlerOutput


class NoteDeleteIArgs(HandlerArgsBase):
    uid: NoteUid
    force: bool | None = None


NOTE_DELETE_I_ARGS_CONFIG = ArgsConfig[NoteDeleteIArgs](
    result_cls=NoteDeleteIArgs,
    args=[
        ArgMetaConfig(
            name="uid",
            required=True,
            parser_func=lambda s: NoteUid(uuid.UUID(s)),
        ),
        ArgMetaConfig(
            name="force",
            type_=ArgType.BOOL,
            required=True,
            allow_input_on_empty=True,
            alternative_text=f"Are you sure you want to delete this {Note.get_meta_info().singular_name}?",
            boolean_text="Yes/No",
        ),
    ],
)


class NoteDeleteIHandler(
    HandlerBase[NoteDeleteIArgs],
):
    def _get_args_config(self) -> ArgsConfig[NoteDeleteIArgs]:
        return NOTE_DELETE_I_ARGS_CONFIG

    def _make_action(self, parsed_args: NoteDeleteIArgs) -> HandlerOutput | None:
        if not parsed_args.force:
            render_canceled_message(
                self.console,
                f"{Note.get_meta_info().singular_name} delete operation cancelled by user.",
            )
            return None

        note_delete(data_storage=self.data_storage, note_uid=parsed_args.uid)

        render_good_message(
            self.console,
            f"{Note.get_meta_info().singular_name} with uid {parsed_args.uid} has been deleted.",
        )

        return None
