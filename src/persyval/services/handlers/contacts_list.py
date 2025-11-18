from typing import TYPE_CHECKING

from persyval.models.contact import (
    Contact,
)
from persyval.services.data_actions.contacts_list import (
    contacts_list,
)
from persyval.services.handlers.contacts.contact_item_ask_next_action import (
    contact_item_ask_next_action,
)
from persyval.services.handlers.shared.list_show import list_show
from persyval.services.handlers.shared.sort_and_filter import (
    LIST_I_ARGS_CONFIG_CONTACTS,
    ListConfig,
    ListIArgs,
)
from persyval.services.handlers_base.handler_base import HandlerBase

if TYPE_CHECKING:
    from persyval.services.commands.args_config import ArgsConfig


# TODO: Make repeatable filtering without exiting to main menu


class ContactsListIHandler(
    HandlerBase[ListIArgs],
):
    def _get_args_config(self) -> ArgsConfig[ListIArgs]:
        return LIST_I_ARGS_CONFIG_CONTACTS

    def _make_action(self, parsed_args: ListIArgs) -> None:
        return list_show(
            list_config=ListConfig(
                **parsed_args.model_dump(),
            ),
            data_storage=self.data_storage,
            list_callable=contacts_list,
            next_action=contact_item_ask_next_action,
            #
            model=Contact,
            console=self.console,
            execution_queue=self.execution_queue,
            #
            plain_render=self.plain_render,
            non_interactive=self.non_interactive,
        )
