import copy
import enum
from typing import TYPE_CHECKING

from prompt_toolkit import HTML, choice, prompt

from persyval.models.contact import Contact, ContactUid, format_birthday, parse_birthday
from persyval.services.data_actions.contact_get import contact_get
from persyval.services.data_actions.contact_list import LIST_FILTER_MODE_REGISTRY, ContactsListConfig, contact_list
from persyval.services.data_actions.contact_update import contact_update
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.services.handlers_base.helpers.no_direct_args_check import no_direct_args_check
from persyval.utils.format import render_good_message

if TYPE_CHECKING:
    from persyval.services.console.types import PromptToolkitFormattedText
    from persyval.services.data_storage.data_storage import DataStorage
    from persyval.services.handlers_base.handler_output import HandlerOutput


class ContactItemAction(enum.StrEnum):
    EDIT = "edit"
    DELETE = "delete"
    VIEW = "view"


class ContactListIHandler(
    HandlerBase,
):
    def _handler(self) -> HandlerOutput | None:
        # TODO: (?) Use optional direct args?
        no_direct_args_check(self.args)

        choice_filter = choice(
            message="Choose filter mode:",
            options=[(item.mode, item.title) for item in LIST_FILTER_MODE_REGISTRY.values()],
        )

        list_config = ContactsListConfig(
            filter_mode=choice_filter,
        )

        contacts = contact_list(
            data_storage=self.data_storage,
            list_config=list_config,
        )

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
                    "Success",
                )

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

    contact.name = name
    contact.address = address
    contact.birthday = parse_birthday(birthday) if birthday else None

    return contact_update(
        data_storage=data_storage,
        contact=contact,
    )
