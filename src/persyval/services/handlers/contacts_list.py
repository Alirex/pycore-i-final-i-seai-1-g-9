from typing import TYPE_CHECKING

from prompt_toolkit import choice, print_formatted_text, prompt

from persyval.exceptions.main import InvalidCommandError
from persyval.models.contact import (
    ALLOWED_KEYS_TO_FILTER,
    AllowedKeysToFilter,
    Contact,
    ContactUid,
)
from persyval.services.console.add_option_i_to_main_menu import (
    add_option_i_to_main_menu,
)
from persyval.services.data_actions.contacts_list import (
    ContactsListConfig,
    contacts_list,
)
from persyval.services.handlers.contacts.contact_item_ask_next_action import (
    contact_item_ask_next_action,
)
from persyval.services.handlers.shared.sort_and_filter import (
    LIST_FILTER_MODE_REGISTRY,
    LIST_I_ARGS_CONFIG,
    ListFilterModeEnum,
    ListIArgs,
)
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_canceled_message

if TYPE_CHECKING:
    from persyval.services.commands.args_config import ArgsConfig
    from persyval.services.console.types import PromptToolkitFormattedText


def parse_queries(queries: list[str]) -> dict[AllowedKeysToFilter, str]:
    result = {}
    for part in queries:
        split = part.split("=")
        if len(split) != 2:  # noqa: PLR2004
            continue

        key, value = split
        key_ = AllowedKeysToFilter(key)
        result[key_] = value

    return result


# TODO: Make repeatable filtering without exiting to main menu


class ContactsListIHandler(
    HandlerBase[ListIArgs],
):
    def _get_args_config(self) -> ArgsConfig[ListIArgs]:
        return LIST_I_ARGS_CONFIG

    def _make_action(self, parsed_args: ListIArgs) -> None:  # noqa: C901, PLR0912
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
                    "Format: key=value,key2=value2 (e.g., name=John,address=UA)\n"
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

            if not parsed_queries:
                msg = "Queries are required."
                raise InvalidCommandError(msg)

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
                f"No {Contact.get_meta_info().plural_name.lower()} found.",
                title="Not found",
            )
            return

        options_list: list[tuple[ContactUid | None, PromptToolkitFormattedText]] = []
        add_option_i_to_main_menu(options_list)

        options_list.extend((contact.uid, contact.get_prompt_toolkit_output()) for contact in contacts)

        message_after_filter = (
            f"{Contact.get_meta_info().plural_name} found: {len(contacts)}. \nChoose one to interact:"
        )
        choice_by_list = choice(
            message=message_after_filter,
            options=options_list,
        )

        if choice_by_list is None:
            return

        contact_item_ask_next_action(
            execution_queue=self.execution_queue,
            uid=choice_by_list,
        )

        return
