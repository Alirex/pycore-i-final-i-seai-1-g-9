import enum
from typing import TYPE_CHECKING

from prompt_toolkit import choice
from pydantic import BaseModel

from persyval.services.commands.commands_enum import Command
from persyval.services.console.add_option_i_to_main_menu import (
    add_option_i_to_main_menu,
)
from persyval.services.execution_queue.execution_queue import (
    ExecutionQueue,
    HandlerFullArgs,
)

if TYPE_CHECKING:
    from persyval.models.note import NoteUid
    from persyval.services.console.types import PromptToolkitFormattedText


@enum.unique
class NoteItemAction(enum.StrEnum):
    VIEW = "view"
    EDIT = "edit"
    DELETE = "delete"


class ChoiceItemMeta(BaseModel):
    action: NoteItemAction
    title: str


CHOICE_ITEM_ORDER = [
    NoteItemAction.VIEW,
    NoteItemAction.EDIT,
    NoteItemAction.DELETE,
]
CHOICE_ITEM_META_REGISTRY: dict[NoteItemAction, ChoiceItemMeta] = {
    item.action: item
    for item in [
        ChoiceItemMeta(
            action=NoteItemAction.VIEW,
            title="View",
        ),
        ChoiceItemMeta(
            action=NoteItemAction.EDIT,
            title="Edit",
        ),
        ChoiceItemMeta(
            action=NoteItemAction.DELETE,
            title="Delete",
        ),
    ]
}


def note_item_ask_next_action(
    *,
    execution_queue: ExecutionQueue,
    uid: NoteUid,
    is_from_view: bool = False,
) -> None:
    options: list[tuple[NoteItemAction | None, PromptToolkitFormattedText]] = []
    for item in CHOICE_ITEM_ORDER:
        if item == NoteItemAction.VIEW and is_from_view:
            continue

        meta = CHOICE_ITEM_META_REGISTRY[item]
        options.append((item, meta.title))

    add_option_i_to_main_menu(options)

    choice_for_item = choice(
        message="What to do with note:",
        options=options,
    )

    match choice_for_item:
        # TODO: (?) Use lazy import, when available. https://peps.python.org/pep-0810/
        case None:
            return

        case NoteItemAction.VIEW:
            from persyval.services.handlers.note_view import (  # noqa: PLC0415
                NoteViewIArgs,
            )

            execution_queue.put(
                HandlerFullArgs(
                    command=Command.NOTE_VIEW,
                    args=NoteViewIArgs(
                        uid=uid,
                    ),
                ),
            )
        case NoteItemAction.EDIT:
            from persyval.services.handlers.note_edit import NoteEditIArgs  # noqa: PLC0415

            execution_queue.put(
                HandlerFullArgs(
                    command=Command.NOTE_EDIT,
                    args=NoteEditIArgs(
                        uid=uid,
                    ),
                ),
            )
        case NoteItemAction.DELETE:
            from persyval.services.handlers.note_delete import NoteDeleteIArgs  # noqa: PLC0415

            execution_queue.put(
                HandlerFullArgs(
                    command=Command.NOTE_DELETE,
                    args=NoteDeleteIArgs(
                        uid=uid,
                    ),
                ),
            )
