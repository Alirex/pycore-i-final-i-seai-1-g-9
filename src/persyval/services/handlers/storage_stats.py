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

        table = Table(title="Storage Stats", title_justify="left")
        table.add_column("Name")
        table.add_column("Amount")

        table.add_row(
            "Contacts",
            str(len(self.data_storage.data.contacts)),
        )

        table.add_row(
            "Notes",
            str(len(self.data_storage.data.notes)),
        )

        self.console.print(table)

        return None
