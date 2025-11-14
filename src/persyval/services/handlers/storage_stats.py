from typing import TYPE_CHECKING

from rich.table import Table

from persyval.services.handlers.shared.args_i_empty import ARGS_CONFIG_I_EMPTY, ArgsIEmpty
from persyval.services.handlers_base.handler_base import HandlerBase

if TYPE_CHECKING:
    from persyval.services.commands.command_meta import ArgsConfig


class StorageStatsIHandler(
    HandlerBase[ArgsIEmpty],
):
    def _get_args_config(self) -> ArgsConfig[ArgsIEmpty]:
        return ARGS_CONFIG_I_EMPTY

    def _make_action(
        self,
        parsed_args: ArgsIEmpty,  # noqa: ARG002
    ) -> None:
        table = Table(title="Storage Stats", title_justify="left")
        table.add_column("Name")
        table.add_column("Amount")

        for info in self.data_storage.get_stats():
            table.add_row(
                info.name,
                str(info.amount),
            )

        self.console.print(table)
