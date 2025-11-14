import uuid
from typing import TYPE_CHECKING

from prompt_toolkit.shortcuts import yes_no_dialog

from persyval.models.note import (
    NoteUid,
)
from persyval.services.commands.command_meta import ArgMetaConfig, ArgsConfig, ArgType
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
        ),
    ],
)


class NoteDeleteIHandler(
    HandlerBase[NoteDeleteIArgs],
):
    def _get_args_config(self) -> ArgsConfig[NoteDeleteIArgs]:
        return NOTE_DELETE_I_ARGS_CONFIG

    def _make_action(self, parsed_args: NoteDeleteIArgs) -> HandlerOutput | None:
        if parsed_args.force is None:
            is_do = yes_no_dialog(
                title="Confirm Note Delete",
                text="Are you sure you want to delete the note?",
            ).run()

        else:
            is_do = parsed_args.force

        if not is_do:
            render_canceled_message(
                self.console,
                "Note delete operation cancelled by user.",
            )
            return None

        note_delete(data_storage=self.data_storage, note_uid=parsed_args.uid)

        render_good_message(
            self.console,
            f"Note with uid {parsed_args.uid} has been removed.",
        )

        return None
