from typing import TYPE_CHECKING

from persyval.exceptions.main import NotFoundError
from persyval.models.contact import Contact

if TYPE_CHECKING:
    from persyval.services.data_storage.data_storage import DataStorage


def contact_update(
    data_storage: DataStorage,
    contact: Contact,
) -> Contact:
    try:
        with data_storage.autosave():
            data_storage.data.contacts[contact.uid] = contact
    except KeyError as exc:
        msg = f"{Contact.get_meta_info().singular_name} with uid {contact.uid} not found."
        raise NotFoundError(msg) from exc

    return contact
