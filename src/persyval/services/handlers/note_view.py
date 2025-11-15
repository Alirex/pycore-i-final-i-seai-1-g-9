from typing import TYPE_CHECKING

from persyval.models.note import Note, NoteUid
from persyval.services.commands.args_config import ArgMetaConfig, ArgsConfig
from persyval.services.console.render_item_card_with_panel import (
    RenderItem,
    render_item_card_with_panel,
)
from persyval.services.data_actions.note_get import note_get
from persyval.services.execution_queue.execution_queue import HandlerArgsBase
from persyval.services.handlers.notes.note_item_ask_next_action import (
    note_item_ask_next_action,
)
from persyval.services.handlers_base.handler_base import HandlerBase

if TYPE_CHECKING:
    from rich.console import Console


class NoteViewIArgs(HandlerArgsBase):
    uid: NoteUid


NOTE_VIEW_I_ARGS_CONFIG = ArgsConfig[NoteViewIArgs](
    result_cls=NoteViewIArgs,
    args=[
        ArgMetaConfig(
            name="uid",
            required=True,
        ),
    ],
)


class NoteViewIHandler(
    HandlerBase[NoteViewIArgs],
):
    def _get_args_config(self) -> ArgsConfig[NoteViewIArgs]:
        return NOTE_VIEW_I_ARGS_CONFIG

    def _make_action(self, parsed_args: NoteViewIArgs) -> None:
        uid = parsed_args.uid

        item = note_get(
            data_storage=self.data_storage,
            uid=uid,
        )

        render_details(
            console=self.console,
            note=item,
        )

        if self.non_interactive:
            return

        note_item_ask_next_action(
            execution_queue=self.execution_queue,
            uid=uid,
            is_from_view=True,
        )


NO_TITLE = "[No Title]"
NO_CONTENT = "[No Content]"


def render_details(console: Console, note: Note) -> None:
    title = (note.title or "").strip() or NO_TITLE
    content = (note.content or "").strip() or NO_CONTENT

    render_item_card_with_panel(
        console=console,
        entity_title=note.get_meta_info().singular_name,
        list_to_render=[
            RenderItem(name="Title", value=title),
            RenderItem(name="Content", value=content),
            # TODO: Tags
            RenderItem(name="Uid", value=str(note.uid)),
        ],
    )
