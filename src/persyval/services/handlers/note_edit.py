import copy
from typing import TYPE_CHECKING

from persyval.models.note import NoteUid
from persyval.services.commands.args_config import ArgMetaConfig, ArgsConfig
from persyval.services.data_actions.note_get import note_get
from persyval.services.execution_queue.execution_queue import HandlerArgsBase
from persyval.services.handlers.notes.add_and_edit import note_edit_for_handler
from persyval.services.handlers.notes.note_item_ask_next_action import note_item_ask_next_action
from persyval.services.handlers_base.handler_base import HandlerBase

if TYPE_CHECKING:
    from persyval.services.handlers_base.handler_output import HandlerOutput


class NoteEditIArgs(HandlerArgsBase):
    uid: NoteUid
    force: bool | None = None


NOTE_EDIT_I_ARGS_CONFIG = ArgsConfig[NoteEditIArgs](
    result_cls=NoteEditIArgs,
    args=[
        ArgMetaConfig(
            name="uid",
            required=True,
        ),
    ],
)


class NoteEditIHandler(
    HandlerBase[NoteEditIArgs],
):
    def _get_args_config(self) -> ArgsConfig[NoteEditIArgs]:
        return NOTE_EDIT_I_ARGS_CONFIG

    def _make_action(self, parsed_args: NoteEditIArgs) -> HandlerOutput | None:
        item = copy.deepcopy(
            note_get(
                data_storage=self.data_storage,
                uid=parsed_args.uid,
            ),
        )
        # TODO: Rework to use ArgsConfig input handling

        note_edit_for_handler(
            console=self.console,
            data_storage=self.data_storage,
            note=item,
        )

        note_item_ask_next_action(
            execution_queue=self.execution_queue,
            uid=item.uid,
        )

        return None
