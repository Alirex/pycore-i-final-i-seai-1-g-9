import enum

from prompt_toolkit import choice

from persyval.services.commands.command_meta import ArgMetaConfig, ArgsConfig
from persyval.services.execution_queue.execution_queue import HandlerArgsBase
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.convert_snake_case_to_human_readable import convert_snake_case_to_human_readable


@enum.unique
class ContactsRootIAction(enum.StrEnum):
    LIST = "list"
    ADD = "add"
    GET_UPCOMING_BIRTHDAYS = "get_upcoming_birthdays"


class ContactsRootIArgs(HandlerArgsBase):
    action: ContactsRootIAction | None = None


CONTACTS_ROOT_I_ARGS_CONFIG = ArgsConfig[ContactsRootIArgs](
    result_cls=ContactsRootIArgs,
    args=[
        ArgMetaConfig(
            name="action",
        ),
    ],
)


class ContactsRootIHandler(
    HandlerBase[ContactsRootIArgs],
):
    def _get_args_config(self) -> ArgsConfig[ContactsRootIArgs]:
        return CONTACTS_ROOT_I_ARGS_CONFIG

    def _make_action(self, parsed_args: ContactsRootIArgs) -> None:
        if parsed_args.action is not None:
            choice_result = parsed_args.action
        else:
            choice_result = choice(
                message="Choose action:",
                options=[(item, convert_snake_case_to_human_readable(item)) for item in ContactsRootIAction],
            )

        match choice_result:
            case ContactsRootIAction.LIST:
                from persyval.services.handlers.contacts_list import (  # noqa: PLC0415
                    CONTACTS_LIST_I_ARGS_CONFIG,
                    ContactsListIHandler,
                )

                ContactsListIHandler(
                    **(self.model_dump() | {"args": []}),
                ).parsed_call(
                    CONTACTS_LIST_I_ARGS_CONFIG.parse([]),
                )
            case ContactsRootIAction.ADD:
                from persyval.services.handlers.contact_add import (  # noqa: PLC0415
                    CONTACT_ADD_I_ARGS_CONFIG,
                    ContactAddIHandler,
                )

                ContactAddIHandler(
                    **(self.model_dump() | {"args": []}),
                ).parsed_call(
                    CONTACT_ADD_I_ARGS_CONFIG.parse([]),
                )
            case ContactsRootIAction.GET_UPCOMING_BIRTHDAYS:
                from persyval.services.handlers.contacts_get_upcoming_birthdays import (  # noqa: PLC0415
                    CONTACTS_GET_BIRTHDAYS_I_ARGS_CONFIG,
                    ContactsGetUpcomingBirthdaysIHandler,
                )

                ContactsGetUpcomingBirthdaysIHandler(
                    **(self.model_dump() | {"args": []}),
                ).parsed_call(
                    CONTACTS_GET_BIRTHDAYS_I_ARGS_CONFIG.parse([]),
                )
