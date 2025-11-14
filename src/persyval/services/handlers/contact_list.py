import copy
import enum
from typing import TYPE_CHECKING, Annotated

from prompt_toolkit import HTML, choice, print_formatted_text, prompt
from pydantic import BaseModel, Field

from persyval.exceptions.main import InvalidCommandError
from persyval.models.contact import (
    ALLOWED_KEYS_TO_FILTER,
    Contact,
    ContactUid,
    format_birthday,
    parse_birthday,
    validate_email_list,
    validate_phone_list,
)
from persyval.services.commands.command_meta import ArgMetaConfig, ArgsConfig, ArgType
from persyval.services.data_actions.contact_get import contact_get
from persyval.services.data_actions.contact_list import (
    LIST_FILTER_MODE_REGISTRY,
    ContactsListConfig,
    ListFilterModeEnum,
    contact_list,
)
from persyval.services.data_actions.contact_update import contact_update
from persyval.services.handlers.contact_view import ContactViewHandler
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_good_message

if TYPE_CHECKING:
    from persyval.services.console.types import PromptToolkitFormattedText
    from persyval.services.data_storage.data_storage import DataStorage
    from persyval.services.handlers_base.handler_output import HandlerOutput


class ContactItemAction(enum.StrEnum):
    EDIT = "edit"
    DELETE = "delete"
    VIEW = "view"


class FilterModeEnum(enum.StrEnum):
    ALL = "all"
    FILTER = "filter"


class PhoneListIArgs(BaseModel):
    filter_mode: ListFilterModeEnum | None = None
    queries: Annotated[list[str], Field(default_factory=list)]


CONTACT_LIST_I_ARGS_CONFIG = ArgsConfig[PhoneListIArgs](
    result_cls=PhoneListIArgs,
    args=[
        ArgMetaConfig(
            name="filter_mode",
            parser_func=lambda x: ListFilterModeEnum(x) if x else None,
        ),
        ArgMetaConfig(
            name="queries",
            type_=ArgType.LIST_BY_COMMA,
        ),
    ],
)


def parse_queries(queries: list[str]) -> dict[str, str]:
    result = {}
    for part in queries:
        key, value = part.split("=")
        result[key] = value

    return result


class ContactListIHandler(
    HandlerBase,
):
    def _handler(self) -> HandlerOutput | None:  # noqa: C901, PLR0912
        # TODO: Refactor this function.
        parsed_args = CONTACT_LIST_I_ARGS_CONFIG.parse(self.args)

        if parsed_args.filter_mode is None and self.non_interactive:
            msg = "Filter mode is required."
            raise InvalidCommandError(msg)
        if parsed_args.filter_mode is not None:
            choice_filter = parsed_args.filter_mode
        else:
            choice_filter = choice(
                message="Choose filter mode:",
                options=[(item.mode, item.title) for item in LIST_FILTER_MODE_REGISTRY.values()],
            )

        if choice_filter is ListFilterModeEnum.FILTER:
            queries = parsed_args.queries
            if not queries:
                msg = "Queries are required."
                raise InvalidCommandError(msg)
            parsed_queries = parse_queries(queries)
            for key in parsed_queries:
                if key not in ALLOWED_KEYS_TO_FILTER:
                    msg = f"Filtering by '{key}' is not allowed."
                    raise InvalidCommandError(msg)

        else:
            parsed_queries = {}

        list_config = ContactsListConfig(
            filter_mode=choice_filter,
            queries_as_map=parsed_queries,
        )

        contacts = contact_list(
            data_storage=self.data_storage,
            list_config=list_config,
        )

        if self.plain_render:
            for contact in contacts:
                print(contact.uid)
            return None

        if self.non_interactive:
            for contact in contacts:
                print_formatted_text(contact.get_prompt_toolkit_output())

            return None

        options_list: list[tuple[ContactUid | None, PromptToolkitFormattedText]] = [
            (None, "Exit"),
        ]
        options_list.extend((contact.uid, contact.get_prompt_toolkit_output()) for contact in contacts)

        choice_by_list = choice(
            message="Choose contact for interact:",
            options=options_list,
        )

        if choice_by_list is None:
            return None

        choice_for_item = choice(
            message="What to do with contact:",
            options=[
                (ContactItemAction.EDIT, "Edit"),
                (ContactItemAction.DELETE, "Delete"),
                (ContactItemAction.VIEW, "View"),
            ],
        )

        match choice_for_item:
            case ContactItemAction.EDIT:
                contact = contact_edit(
                    data_storage=self.data_storage,
                    contact_uid=choice_by_list,
                )

                render_good_message(
                    self.console,
                    f"Contact '{contact.name}' edited successfully.",
                )

            case ContactItemAction.VIEW:
                return ContactViewHandler(
                    console=self.console,
                    data_storage=self.data_storage,
                    args=[str(choice_by_list)],
                ).run()

            case _:
                raise NotImplementedError

        return None


def contact_edit(
    data_storage: DataStorage,
    contact_uid: ContactUid,
) -> Contact:
    contact = copy.deepcopy(
        contact_get(
            data_storage=data_storage,
            contact_uid=contact_uid,
        ),
    )

    name = prompt(
        message=HTML("<b>Name</b>: "),
        default=str(contact.name),
    )
    address = prompt(
        message=HTML("<b>Address</b>: "),
        default=str(contact.address) if contact.address else "",
    )
    birthday = prompt(
        message=HTML("<b>Birthday</b> (YYYY-MM-DD): "),
        default=format_birthday(contact.birthday) if contact.birthday else "",
    )

    phones_input = prompt(
        message=HTML("<b>Phones</b>: "),
        default=",".join(contact.phones) if contact.phones else "",
    )

    phones_list = [phone.strip() for phone in phones_input.split(",") if phone.strip()]

    emails_input = prompt(
        message=HTML("<b>Emails</b>: "),
        default=",".join(contact.emails) if contact.emails else "",
    )

    emails_list = [email.strip() for email in emails_input.split(",") if email.strip()]

    contact.name = name
    contact.address = address
    contact.birthday = parse_birthday(birthday) if birthday else None
    contact.phones = validate_phone_list(phones_list)
    contact.emails = validate_email_list(emails_list)

    return contact_update(
        data_storage=data_storage,
        contact=contact,
    )
