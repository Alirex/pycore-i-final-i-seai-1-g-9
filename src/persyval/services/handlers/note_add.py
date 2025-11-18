from typing import TYPE_CHECKING

from persyval.services.handlers.notes.add_and_edit import note_add_for_handler
from persyval.services.handlers.notes.note_item_ask_next_action import note_item_ask_next_action
from persyval.services.handlers.shared.args_i_empty import ARGS_CONFIG_I_EMPTY, ArgsIEmpty
from persyval.services.handlers_base.handler_base import HandlerBase

if TYPE_CHECKING:
    from persyval.services.commands.args_config import ArgsConfig


# class NoteAddIArgs(HandlerArgsBase):
#     uid: NoteUid
#     force: bool | None = None
#
#
# NOTE_ADD_I_ARGS_CONFIG = ArgsConfig[NoteAddIArgs](
#     result_cls=NoteAddIArgs,
#     args=[
#         ArgMetaConfig(
#             name="title",
#             required=True,
#         ),
#     ],
# )


class NoteAddIHandler(
    HandlerBase[ArgsIEmpty],
):
    def _get_args_config(self) -> ArgsConfig[ArgsIEmpty]:
        return ARGS_CONFIG_I_EMPTY

    def _make_action(
        self,
        parsed_args: ArgsIEmpty,  # noqa: ARG002
    ) -> None:
        # TODO: Rework to use ArgsConfig input handling
        note_or_none = note_add_for_handler(
            console=self.console,
            data_storage=self.data_storage,
        )

        if note_or_none is None:
            return

        if self.non_interactive:
            return

        note_item_ask_next_action(
            execution_queue=self.execution_queue,
            uid=note_or_none.uid,
        )

        return
