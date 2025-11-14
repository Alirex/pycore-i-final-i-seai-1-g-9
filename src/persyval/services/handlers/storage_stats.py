from typing import TYPE_CHECKING

from rich.table import Table

from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.services.handlers_base.helpers.no_direct_args_check import (
    no_direct_args_check,
)

if TYPE_CHECKING:
    from persyval.services.handlers_base.handler_output import HandlerOutput


class StorageStatsIHandler(
    HandlerBase,
):
    def _handler(self) -> HandlerOutput | None:
        no_direct_args_check(self.args)
        self._make_action(None)
        return None

    def parsed_call(self, parsed_args: None) -> None:
        self._make_action(parsed_args)

    def _make_action(
        self,
        parsed_args: None,  # noqa: ARG002
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
