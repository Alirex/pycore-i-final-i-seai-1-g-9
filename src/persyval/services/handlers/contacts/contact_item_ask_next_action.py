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
    from persyval.models.contact import ContactUid
    from persyval.services.console.types import PromptToolkitFormattedText


@enum.unique
class ContactItemAction(enum.StrEnum):
    VIEW = "view"
    EDIT = "edit"
    DELETE = "delete"


class ChoiceItemMeta(BaseModel):
    action: ContactItemAction
    title: str


CHOICE_ITEM_ORDER = [
    ContactItemAction.VIEW,
    ContactItemAction.EDIT,
    ContactItemAction.DELETE,
]
CHOICE_ITEM_META_REGISTRY: dict[ContactItemAction, ChoiceItemMeta] = {
    item.action: item
    for item in [
        ChoiceItemMeta(
            action=ContactItemAction.VIEW,
            title="View",
        ),
        ChoiceItemMeta(
            action=ContactItemAction.EDIT,
            title="Edit",
        ),
        ChoiceItemMeta(
            action=ContactItemAction.DELETE,
            title="Delete",
        ),
    ]
}


def contact_item_ask_next_action(
    *,
    execution_queue: ExecutionQueue,
    uid: ContactUid,
    is_from_view: bool = False,
) -> None:
    options: list[tuple[ContactItemAction | None, PromptToolkitFormattedText]] = []
    for item in CHOICE_ITEM_ORDER:
        if item == ContactItemAction.VIEW and is_from_view:
            continue

        meta = CHOICE_ITEM_META_REGISTRY[item]
        options.append((item, meta.title))

    add_option_i_to_main_menu(options)

    choice_for_item = choice(
        message="What to do with contact:",
        options=options,
    )

    match choice_for_item:
        # TODO: (?) Use lazy import, when available. https://peps.python.org/pep-0810/
        case None:
            return

        case ContactItemAction.VIEW:
            from persyval.services.handlers.contact_view import (  # noqa: PLC0415
                ContactViewIArgs,
            )

            execution_queue.put(
                HandlerFullArgs(
                    command=Command.CONTACT_VIEW,
                    args=ContactViewIArgs(
                        uid=uid,
                    ),
                ),
            )
        case ContactItemAction.EDIT:
            from persyval.services.handlers.contact_edit import (  # noqa: PLC0415
                ContactEditIArgs,
            )

            execution_queue.put(
                HandlerFullArgs(
                    command=Command.CONTACT_EDIT,
                    args=ContactEditIArgs(
                        uid=uid,
                    ),
                ),
            )
        case ContactItemAction.DELETE:
            from persyval.services.handlers.contact_delete import (  # noqa: PLC0415
                ContactDeleteIArgs,
            )

            execution_queue.put(
                HandlerFullArgs(
                    command=Command.CONTACT_DELETE,
                    args=ContactDeleteIArgs(
                        uid=uid,
                    ),
                ),
            )
