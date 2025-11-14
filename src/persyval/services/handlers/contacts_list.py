import enum
from typing import TYPE_CHECKING

from prompt_toolkit import choice, print_formatted_text, prompt

from persyval.constants.text import CHOICE_I_TO_MAIN_MENU
from persyval.exceptions.main import InvalidCommandError
from persyval.models.contact import (
    ALLOWED_KEYS_TO_FILTER,
    ContactUid,
)
from persyval.services.commands.args_config import ArgMetaConfig, ArgsConfig, ArgType
from persyval.services.data_actions.contacts_list import (
    LIST_FILTER_MODE_REGISTRY,
    ContactsListConfig,
    ListFilterModeEnum,
    contacts_list,
)
from persyval.services.execution_queue.execution_queue import HandlerArgsBase
from persyval.services.handlers.contacts.contacts_ask_next_action import contacts_ask_next_action
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_canceled_message

if TYPE_CHECKING:
    from persyval.services.console.types import PromptToolkitFormattedText


@enum.unique
class FilterModeEnum(enum.StrEnum):
    ALL = "all"
    FILTER = "filter"


class ContactsListIArgs(HandlerArgsBase):
    filter_mode: ListFilterModeEnum | None = None
    queries: list[str] | None = None


CONTACTS_LIST_I_ARGS_CONFIG = ArgsConfig[ContactsListIArgs](
    result_cls=ContactsListIArgs,
    args=[
        ArgMetaConfig(
            name="filter_mode",
            parser_func=lambda x: ListFilterModeEnum(x) if x else None,
        ),
        ArgMetaConfig(
            name="queries",
            type_=ArgType.LIST_BY_COMMA,
            default_factory=list,
        ),
    ],
)


def parse_queries(queries: list[str]) -> dict[str, str]:
    result = {}
    for part in queries:
        key, value = part.split("=")
        result[key] = value

    return result


# TODO: Make repeatable filtering without exiting to main menu


class ContactsListIHandler(
    HandlerBase[ContactsListIArgs],
):
    def _get_args_config(self) -> ArgsConfig[ContactsListIArgs]:
        return CONTACTS_LIST_I_ARGS_CONFIG

    def _make_action(self, parsed_args: ContactsListIArgs) -> None:  # noqa: C901, PLR0912
        if parsed_args.filter_mode is None and self.non_interactive:
            msg = "Filter mode is required."
            raise InvalidCommandError(msg)

        if parsed_args.filter_mode is not None:
            choice_filter = parsed_args.filter_mode
        else:
            choice_filter = choice(
                message="Choose filter mode:",
                options=[(item.mode, item.title) for item in LIST_FILTER_MODE_REGISTRY.values()],
            )

        if choice_filter is ListFilterModeEnum.FILTER:
            queries = parsed_args.queries
            if not queries:
                message = (
                    "Enter queries to filter by. \n"
                    "Format: key=value,key2=value2 (e.g., name=John,address=UA \n"
                    f"Allowed keys: {', '.join(sorted(ALLOWED_KEYS_TO_FILTER))}\n"
                )
                queries_raw = prompt(
                    message=message,
                )
                queries = queries_raw.split(",")

            if not queries:
                msg = "Queries are required."
                raise InvalidCommandError(msg)

            parsed_queries = parse_queries(queries)
            for key in parsed_queries:
                if key not in ALLOWED_KEYS_TO_FILTER:
                    msg = f"Filtering by '{key}' is not allowed."
                    raise InvalidCommandError(msg)

        else:
            parsed_queries = {}

        list_config = ContactsListConfig(
            filter_mode=choice_filter,
            queries_as_map=parsed_queries,
        )

        contacts = contacts_list(
            data_storage=self.data_storage,
            list_config=list_config,
        )

        if self.plain_render:
            for contact in contacts:
                print(contact.uid)
            return

        if self.non_interactive:
            for contact in contacts:
                print_formatted_text(contact.get_prompt_toolkit_output())

            return

        if not contacts:
            render_canceled_message(
                self.console,
                "No contacts found.",
                title="Not found",
            )
            return

        options_list: list[tuple[ContactUid | None, PromptToolkitFormattedText]] = [
            (None, CHOICE_I_TO_MAIN_MENU),
        ]
        options_list.extend((contact.uid, contact.get_prompt_toolkit_output()) for contact in contacts)

        message_after_filter = f"Contacts found: {len(contacts)}. \nChoose one to interact:"
        choice_by_list = choice(
            message=message_after_filter,
            options=options_list,
        )

        if choice_by_list is None:
            return

        contacts_ask_next_action(
            execution_queue=self.execution_queue,
            contact_uid=choice_by_list,
        )

        return
