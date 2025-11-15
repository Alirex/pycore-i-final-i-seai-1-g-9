from typing import TYPE_CHECKING, Final

from persyval.models.contact import Contact
from persyval.services.data_actions.contacts_list import ContactsListConfig, ListFilterModeEnum, contacts_list
from persyval.services.export.export_items import write_to_csv
from persyval.services.get_paths.get_app_dirs import get_downloads_dir_in_user_space
from persyval.services.handlers.shared.args_i_empty import (
    ARGS_CONFIG_I_EMPTY,
    ArgsIEmpty,
)
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_canceled_message, render_good_message

if TYPE_CHECKING:
    from persyval.services.commands.args_config import ArgsConfig


class ContactsExportIHandler(HandlerBase[ArgsIEmpty]):
    def _get_args_config(self) -> ArgsConfig[ArgsIEmpty]:
        return ARGS_CONFIG_I_EMPTY

    def _make_action(
        self,
        parsed_args: ArgsIEmpty,  # noqa: ARG002
    ) -> None:
        # TODO: (?) Add export to different formats (CSV, JSON).

        # TODO: (?) Add ability to filter data or get all.

        # TODO: (?) Add ability to import data.

        # TODO: (?) Add ability to check path.
        #  If exists, ask for overwrite or provide other not-existing path.

        contacts = contacts_list(
            data_storage=self.data_storage,
            list_config=ContactsListConfig(
                filter_mode=ListFilterModeEnum.ALL,
            ),
        )

        if not contacts:
            render_canceled_message(
                self.console,
                message=f"There are no {Contact.get_meta_info().plural_name.lower()} to export.",
                title="Empty storage",
            )
            return

        extension: Final[str] = "csv"
        base_name: Final[str] = f"{Contact.get_meta_info().plural_name.lower()}.{extension}"

        export_path = get_downloads_dir_in_user_space() / base_name

        if write_to_csv(self.console, contacts, export_path):
            render_good_message(
                self.console,
                f"{Contact.get_meta_info().plural_name} were successfully exported to {export_path.as_uri()}",
            )
