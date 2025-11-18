from typing import TYPE_CHECKING

from persyval.models.note import Note
from persyval.services.data_actions.notes_list import notes_list
from persyval.services.export.export_items import choose_export_format, export_items
from persyval.services.handlers.shared.args_i_empty import (
    ARGS_CONFIG_I_EMPTY,
    ArgsIEmpty,
)
from persyval.services.handlers.shared.sort_and_filter import ListConfig, ListFilterModeEnum, ListOrderModeEnum
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_canceled_message

if TYPE_CHECKING:
    from persyval.services.commands.args_config import ArgsConfig


class NotesExportIHandler(HandlerBase[ArgsIEmpty]):
    def _get_args_config(self) -> ArgsConfig[ArgsIEmpty]:
        return ARGS_CONFIG_I_EMPTY

    def _make_action(
        self,
        parsed_args: ArgsIEmpty,  # noqa: ARG002
    ) -> None:
        chosen_format = choose_export_format(non_interactive=self.non_interactive)
        if chosen_format is None:
            render_canceled_message(self.console, "Export canceled.")
            return

        notes = notes_list(
            data_storage=self.data_storage,
            list_config=ListConfig(
                filter_mode=ListFilterModeEnum.ALL,
                order_mode=ListOrderModeEnum.DEFAULT,
            ),
        )

        if not notes:
            render_canceled_message(
                self.console,
                f"There are no {Note.get_meta_info().plural_name.lower()} to export.",
            )
            return

        export_items(
            console=self.console,
            items=notes,
            file_base_name=Note.get_meta_info().plural_name.lower(),
            chosen_format=chosen_format,
        )
