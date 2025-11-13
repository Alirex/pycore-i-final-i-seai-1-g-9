from typing import TYPE_CHECKING, Annotated, Final

from pydantic import AfterValidator, BaseModel
from rich.table import Table

from persyval.services.birthday.parse_and_format import format_birthday_for_output
from persyval.services.commands.command_meta import ArgMetaConfig, ArgsConfig, ArgType
from persyval.services.data_actions.contacts_get_upcoming_birthdays import contacts_get_upcoming_birthdays
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_canceled_message

if TYPE_CHECKING:
    from persyval.services.handlers_base.handler_output import HandlerOutput

MAX_DAYS_RANGE_TO_SHOW_BIRTHDAYS: Final[int] = 365


def validate_days_to_show_birthdays(days: int) -> int:
    if not 0 < days <= MAX_DAYS_RANGE_TO_SHOW_BIRTHDAYS:
        msg = "Entered value should be between 1 and 365 days."
        raise ValueError(msg)

    return days


class ContactsGetUpcomingBirthdaysIArgs(BaseModel):
    days: Annotated[int, AfterValidator(validate_days_to_show_birthdays)] = 7


CONTACTS_GET_BIRTHDAYS_I_ARGS_CONFIG = ArgsConfig[ContactsGetUpcomingBirthdaysIArgs](
    result_cls=ContactsGetUpcomingBirthdaysIArgs,
    args=[
        ArgMetaConfig(
            name="days",
            type_=ArgType.INT,
            validator_func=validate_days_to_show_birthdays,
        ),
    ],
)


class ContactsGetUpcomingBirthdaysIHandler(
    HandlerBase,
):
    def _handler(self) -> HandlerOutput | None:
        parse_result = CONTACTS_GET_BIRTHDAYS_I_ARGS_CONFIG.parse(self.args)

        upcoming_birthdays = contacts_get_upcoming_birthdays(self.data_storage, parse_result.days, sort=True)

        if not upcoming_birthdays:
            render_canceled_message(
                console=self.console,
                message=f"No upcoming birthdays within indicated period - {parse_result.days} days.",
                title="No birthdays found",
            )
            return None

        table = Table(title="Upcoming birthdays", title_justify="left")
        table.add_column("Name")
        table.add_column("Congratulation date")
        table.add_column("Non-weekend congratulation date")

        for anniversary_info in upcoming_birthdays:
            table.add_row(
                anniversary_info.name,
                format_birthday_for_output(anniversary_info.congratulation_date),
                format_birthday_for_output(anniversary_info.non_weekend_congratulation_date),
            )

        self.console.print(table)

        return None
