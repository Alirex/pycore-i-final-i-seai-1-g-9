from typing import TYPE_CHECKING

from prompt_toolkit import choice, print_formatted_text

from persyval.models.contact import (
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
    LIST_I_ARGS_CONFIG_CONTACTS,
    ListIArgs,
)
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_canceled_message

if TYPE_CHECKING:
    from persyval.services.commands.args_config import ArgsConfig
    from persyval.services.console.types import PromptToolkitFormattedText


# TODO: Make repeatable filtering without exiting to main menu


class ContactsListIHandler(
    HandlerBase[ListIArgs],
):
    def _get_args_config(self) -> ArgsConfig[ListIArgs]:
        return LIST_I_ARGS_CONFIG_CONTACTS

    def _make_action(self, parsed_args: ListIArgs) -> None:
        list_config = ContactsListConfig(
            **parsed_args.model_dump(),
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
