import enum
from typing import TYPE_CHECKING

from prompt_toolkit import choice

from persyval.services.commands.args_config import ArgMetaConfig, ArgsConfig
from persyval.services.commands.commands_enum import Command
from persyval.services.console.add_option_i_to_main_menu import add_option_i_to_main_menu
from persyval.services.execution_queue.execution_queue import (
    HandlerArgsBase,
    HandlerFullArgs,
)
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.convert_snake_case_to_human_readable import (
    convert_snake_case_to_human_readable,
)

if TYPE_CHECKING:
    from persyval.services.console.types import PromptToolkitFormattedText


@enum.unique
class ContactsRootIAction(enum.StrEnum):
    LIST = "list"
    ADD = "add"
    GET_UPCOMING_BIRTHDAYS = "get_upcoming_birthdays"
    EXPORT = "export"


class ContactsRootIArgs(HandlerArgsBase):
    action: ContactsRootIAction | None = None


CONTACTS_ROOT_I_ARGS_CONFIG = ArgsConfig[ContactsRootIArgs](
    result_cls=ContactsRootIArgs,
    args=[
        ArgMetaConfig(
            name="action",
        ),
    ],
)


class ContactsRootIHandler(
    HandlerBase[ContactsRootIArgs],
):
    def _get_args_config(self) -> ArgsConfig[ContactsRootIArgs]:
        return CONTACTS_ROOT_I_ARGS_CONFIG

    def _make_action(self, parsed_args: ContactsRootIArgs) -> None:
        choice_result: ContactsRootIAction | None

        if parsed_args.action is not None:
            choice_result = parsed_args.action
        else:
            options: list[tuple[ContactsRootIAction | None, PromptToolkitFormattedText]] = [
                (item, convert_snake_case_to_human_readable(item)) for item in ContactsRootIAction
            ]
            add_option_i_to_main_menu(options)
            choice_result = choice(
                message="Choose action:",
                options=options,
            )

        if choice_result is None:
            return

        match choice_result:
            # TODO: (?) Use lazy import, when available. https://peps.python.org/pep-0810/
            case ContactsRootIAction.LIST:
                from persyval.services.handlers.shared.sort_and_filter import ListIArgs  # noqa: PLC0415

                self.execution_queue.put(
                    HandlerFullArgs(
                        command=Command.CONTACTS_LIST,
                        args=ListIArgs(),
                    ),
                )

            case ContactsRootIAction.ADD:
                from persyval.services.handlers.contact_add import (  # noqa: PLC0415
                    ContactAddIArgs,
                )

                self.execution_queue.put(
                    HandlerFullArgs(
                        command=Command.CONTACT_ADD,
                        args=ContactAddIArgs(),
                    ),
                )

            case ContactsRootIAction.GET_UPCOMING_BIRTHDAYS:
                from persyval.services.handlers.contacts_get_upcoming_birthdays import (  # noqa: PLC0415
                    ContactsGetUpcomingBirthdaysIArgs,
                )

                self.execution_queue.put(
                    HandlerFullArgs(
                        command=Command.CONTACTS_GET_UPCOMING_BIRTHDAYS,
                        args=ContactsGetUpcomingBirthdaysIArgs(),
                    ),
                )
            case ContactsRootIAction.EXPORT:
                from persyval.services.handlers.shared.args_i_empty import ArgsIEmpty  # noqa: PLC0415

                self.execution_queue.put(
                    HandlerFullArgs(
                        command=Command.CONTACTS_EXPORT,
                        args=ArgsIEmpty(),
                    ),
                )
