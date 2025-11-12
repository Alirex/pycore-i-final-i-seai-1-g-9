from typing import TYPE_CHECKING, cast

from pydantic import BaseModel
from rich.table import Table

from persyval.constants.numeric_contants import YEAR
from persyval.models.contact import format_birthday
from persyval.services.commands.command_meta import ArgMetaConfig, ArgsConfig, ArgType
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_canceled_message

if TYPE_CHECKING:
    from datetime import date

    from persyval.services.handlers_base.handler_output import HandlerOutput


def validate_days_to_show_birthdays(days: int) -> int:
    if not 0 < days <= YEAR:
        msg = "Entered value should be between 1 and 365 days."
        raise ValueError(msg)

    return days


class ShowContactsIArgs(BaseModel):
    days: int = 7


STORAGE_SHOW_BIRTHDAYS_I_ARGS_CONFIG = ArgsConfig[ShowContactsIArgs](
    result_cls=ShowContactsIArgs,
    args=[
        ArgMetaConfig(
            name="days",
            type_=ArgType.INT,
            validator_func=validate_days_to_show_birthdays,
        ),
    ],
)


class StorageShowBirthdaysIHandler(
    HandlerBase,
):
    def _handler(self) -> HandlerOutput | None:
        parse_result = STORAGE_SHOW_BIRTHDAYS_I_ARGS_CONFIG.parse(self.args)

        upcoming_birthdays = self.data_storage.get_upcoming_birthdays(parse_result.days)
        if not upcoming_birthdays:
            render_canceled_message(
                console=self.console,
                message=f"No upcoming birthdays within indicated period - {parse_result.days} days.",
                title="No birthdays found",
            )
            return None

        sorted_birthdays = sorted(upcoming_birthdays, key=lambda person: person["congratulation date"])

        table = Table(title="Upcomig birthdays", title_justify="left")
        table.add_column("Name")
        table.add_column("Congratulation date")
        table.add_column("Non-weekend congratulation date")

        for birthday in sorted_birthdays:
            table.add_row(
                cast("str", birthday["name"]),
                format_birthday(cast("date", birthday["congratulation date"])),
                format_birthday(cast("date", birthday["non-weekend congratulation date"])),
            )

        self.console.print(table)

        return None
