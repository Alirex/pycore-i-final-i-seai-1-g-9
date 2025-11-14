import enum
from typing import TYPE_CHECKING, Annotated

from prompt_toolkit import choice, print_formatted_text, prompt
from pydantic import BaseModel, Field

from persyval.exceptions.main import InvalidCommandError
from persyval.models.contact import (
    ALLOWED_KEYS_TO_FILTER,
    ContactUid,
)
from persyval.services.commands.command_meta import ArgMetaConfig, ArgsConfig, ArgType
from persyval.services.data_actions.contacts_list import (
    LIST_FILTER_MODE_REGISTRY,
    ContactsListConfig,
    ListFilterModeEnum,
    contacts_list,
)
from persyval.services.handlers_base.handler_base import HandlerBase

if TYPE_CHECKING:
    from persyval.services.console.types import PromptToolkitFormattedText
    from persyval.services.handlers_base.handler_output import HandlerOutput


class ContactItemAction(enum.StrEnum):
    EDIT = "edit"
    DELETE = "delete"
    VIEW = "view"


class FilterModeEnum(enum.StrEnum):
    ALL = "all"
    FILTER = "filter"


class ContactsListIArgs(BaseModel):
    filter_mode: ListFilterModeEnum | None = None
    queries: Annotated[list[str], Field(default_factory=list)]


CONTACTS_LIST_I_ARGS_CONFIG = ArgsConfig[ContactsListIArgs](
    result_cls=ContactsListIArgs,
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


class ContactsListIHandler(
    HandlerBase,
):
    def _handler(self) -> HandlerOutput | None:
        # TODO: Refactor this function.
        parsed_args = CONTACTS_LIST_I_ARGS_CONFIG.parse(self.args)
        self._make_action(parsed_args)
        return None

    def parsed_call(self, parsed_args: ContactsListIArgs) -> None:
        self._make_action(parsed_args)

    def _make_action(self, parsed_args: ContactsListIArgs) -> None:  # noqa: C901, PLR0912
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
                queries_raw = prompt(
                    message="Enter queries (a=b,c=d):",
                )
                queries = queries_raw.split(",")

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

        contacts = contacts_list(
            data_storage=self.data_storage,
            list_config=list_config,
        )

        if self.plain_render:
            for contact in contacts:
                print(contact.uid)
            return

        if self.non_interactive:
            for contact in contacts:
                print_formatted_text(contact.get_prompt_toolkit_output())

            return

        options_list: list[tuple[ContactUid | None, PromptToolkitFormattedText]] = [
            (None, "Exit"),
        ]
        options_list.extend((contact.uid, contact.get_prompt_toolkit_output()) for contact in contacts)

        choice_by_list = choice(
            message="Choose contact for interact:",
            options=options_list,
        )

        if choice_by_list is None:
            return

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
                from persyval.services.handlers.contact_edit import (  # noqa: PLC0415
                    ContactEditIArgs,
                    ContactEditIHandler,
                )

                ContactEditIHandler(
                    **(self.model_dump() | {"args": []}),
                ).parsed_call(
                    ContactEditIArgs(
                        uid=choice_by_list,
                    ),
                )

            case ContactItemAction.VIEW:
                from persyval.services.handlers.contact_view import (  # noqa: PLC0415
                    ContactViewIArgs,
                    ContactViewIHandler,
                )

                ContactViewIHandler(
                    **(self.model_dump() | {"args": []}),
                ).parsed_call(
                    ContactViewIArgs(
                        uid=choice_by_list,
                    ),
                )
            case ContactItemAction.DELETE:
                from persyval.services.handlers.contact_delete import (  # noqa: PLC0415
                    ContactDeleteIArgs,
                    ContactDeleteIHandler,
                )

                ContactDeleteIHandler(
                    **(self.model_dump() | {"args": []}),
                ).parsed_call(
                    ContactDeleteIArgs(
                        uid=choice_by_list,
                    ),
                )

            case _:
                raise NotImplementedError

        return
