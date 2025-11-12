from typing import TYPE_CHECKING

from persyval.exceptions.main import NotFoundError

if TYPE_CHECKING:
    from persyval.models.contact import Contact
    from persyval.services.data_storage.data_storage import DataStorage


def contact_update(
    data_storage: DataStorage,
    contact: Contact,
) -> Contact:
    try:
        data_storage.data.contacts[contact.uid] = contact
    except KeyError as exc:
        msg = f"Contact with uid {contact.uid} not found."
        raise NotFoundError(msg) from exc

    return contact
