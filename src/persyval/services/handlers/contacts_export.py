from enum import Enum
from typing import TYPE_CHECKING, Final

from prompt_toolkit.shortcuts import choice

from persyval.models.contact import Contact
from persyval.services.data_actions.contacts_list import ContactsListConfig, contacts_list
from persyval.services.export.export_items import write_to_csv, write_to_json
from persyval.services.get_paths.get_app_dirs import get_downloads_dir_in_user_space
from persyval.services.handlers.shared.args_i_empty import (
    ARGS_CONFIG_I_EMPTY,
    ArgsIEmpty,
)
from persyval.services.handlers.shared.sort_and_filter import ListFilterModeEnum
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_canceled_message, render_error, render_good_message

if TYPE_CHECKING:
    from persyval.services.commands.args_config import ArgsConfig


class ExportFormat(str, Enum):
    CSV = "csv"
    JSON = "json"


class ContactsExportIHandler(HandlerBase[ArgsIEmpty]):
    def _get_args_config(self) -> ArgsConfig[ArgsIEmpty]:
        return ARGS_CONFIG_I_EMPTY

    def _make_action(
        self,
        parsed_args: ArgsIEmpty,  # noqa: ARG002
    ) -> None:
        # TODO: (?) Add ability to filter data or get all.

        # TODO: (?) Add ability to import data.

        # TODO: (?) Implement all of this for notes.

        format_choices = [
            (ExportFormat.CSV, "CSV"),
            (ExportFormat.JSON, "JSON"),
        ]

        chosen_format = choice(
            message="Choose export format",
            options=format_choices,
        )

        if chosen_format is None:
            render_canceled_message(self.console, "Export canceled.")
            return

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

        extension: str = chosen_format.value
        base_name: Final[str] = f"{Contact.get_meta_info().plural_name.lower()}.{extension}"
        export_path = get_downloads_dir_in_user_space() / base_name

        if export_path.exists():
            self.console.print(
                f"[yellow]Warning: The file already exists at this path:\n{export_path.as_uri()}[/yellow]",
            )

            overwrite_choices = [
                (True, "Yes, overwrite the existing file"),
                (False, "No, cancel export"),
            ]

            should_overwrite = choice(
                message="Would you like to continue?",
                options=overwrite_choices,
            )

            if not should_overwrite:
                render_canceled_message(self.console, "Export canceled by user.")
                return

        try:
            if chosen_format == ExportFormat.CSV:
                write_to_csv(items=contacts, path=export_path)
            elif chosen_format == ExportFormat.JSON:
                write_to_json(items=contacts, path=export_path)

        except Exception as exc:  # noqa: BLE001
            render_error(
                self.console,
                title=f"{exc.__class__.__name__}",
                message=f"Error while exporting {Contact.get_meta_info().plural_name} to {export_path.as_uri()}: {exc}",
            )

            return

        render_good_message(
            self.console,
            f"{Contact.get_meta_info().plural_name} were successfully exported to {export_path.as_uri()}",
        )
