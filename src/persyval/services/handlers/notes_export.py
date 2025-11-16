from typing import TYPE_CHECKING, Final

from persyval.models.note import Note
from persyval.services.data_actions.notes_list import NotesListConfig, note_list
from persyval.services.export.export_items import write_to_csv
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


class NotesExportIHandler(HandlerBase[ArgsIEmpty]):
    def _get_args_config(self) -> ArgsConfig[ArgsIEmpty]:
        return ARGS_CONFIG_I_EMPTY

    def _make_action(
        self,
        parsed_args: ArgsIEmpty,  # noqa: ARG002
    ) -> None:
        # TODO: (?) Add export to different formats (with select) (CSV, JSON (by pydantic RootModel ?)).

        # TODO: (?) Add ability to filter data or get all.

        # TODO: (?) Add ability to import data.

        # TODO: (?) Add ability to check path.
        #  If exists, ask for overwrite or provide other not-existing path.

        list_config = NotesListConfig(filter_mode=ListFilterModeEnum.ALL)

        notes = note_list(
            data_storage=self.data_storage,
            list_config=list_config,
        )

        if not notes:
            render_canceled_message(
                self.console,
                message=f"There are no {Note.get_meta_info().plural_name.lower()} to export.",
                title="Empty storage",
            )
            return

        extension: Final[str] = "csv"
        base_name: Final[str] = f"{Note.get_meta_info().plural_name.lower()}.{extension}"

        export_path = get_downloads_dir_in_user_space() / base_name

        try:
            write_to_csv(items=notes, path=export_path)
        except Exception as exc:  # noqa: BLE001
            render_error(
                self.console,
                title=f"{exc.__class__.__name__}",
                message=f"Error while exporting {Note.get_meta_info().plural_name} to {export_path.as_uri()}: {exc}",
            )

        render_good_message(
            self.console,
            f"{Note.get_meta_info().plural_name} were successfully exported to {export_path.as_uri()}",
        )
