from __future__ import annotations

from typing import TYPE_CHECKING, cast
from uuid import UUID

from persyval.services.data_actions.contact_get import contact_get
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_good_message

if TYPE_CHECKING:
    from persyval.models.contact import ContactUid
    from persyval.services.handlers_base.handler_output import HandlerOutput


class ContactViewHandler(HandlerBase):
    def _handler(self) -> HandlerOutput | None:
        raw_uid_str = self.args[0]
        raw_uid = UUID(raw_uid_str)
        contact_uid = cast("ContactUid", raw_uid)

        contact = contact_get(
            data_storage=self.data_storage,
            contact_uid=contact_uid,
        )

        phones = ", ".join(contact.phones) if contact.phones else "-"
        emails = ", ".join(contact.emails) if contact.emails else "-"
        address = contact.address or "-"
        birthday = contact.birthday.isoformat() if contact.birthday else "-"
        message = (
            "Contact details\n"
            f"Name: {contact.name}\n"
            f"Address: {address}\n"
            f"Birthday: {birthday}\n"
            f"Phones: {phones}\n"
            f"Emails: {emails}"
        )

        render_good_message(self.console, message)

        return None
