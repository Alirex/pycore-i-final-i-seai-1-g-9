import pathlib
from typing import TYPE_CHECKING, Final

from persyval.services.data_actions.contacts_download import write_contacts_to_csv
from persyval.services.handlers.contacts_list import CONTACTS_LIST_I_ARGS_CONFIG, ContactsListIArgs
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_canceled_message

if TYPE_CHECKING:
    from persyval.services.commands.args_config import ArgsConfig

DEFAULT_FILENAME_FOR_SAVE: Final[str] = "contacts_export.csv"


class ContactsListDownloadIHandler(HandlerBase[ContactsListIArgs]):
    def _get_args_config(self) -> ArgsConfig[ContactsListIArgs]:
        return CONTACTS_LIST_I_ARGS_CONFIG

    def _make_action(self, parsed_args: ContactsListIArgs) -> None:
        _ = parsed_args
        contacts = list(self.data_storage.data.contacts.values())

        if not contacts:
            render_canceled_message(
                self.console,
                message="There are no contacts to export.",
                title="Empty storage",
            )
            return

        export_path = pathlib.Path.home() / DEFAULT_FILENAME_FOR_SAVE

        if write_contacts_to_csv(self.console, contacts, export_path):
            self.console.print(
                f"[green]Contacts were successfully exported to[/green] {export_path}",
            )
