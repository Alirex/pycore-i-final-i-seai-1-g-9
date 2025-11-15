from typing import TYPE_CHECKING

from persyval.exceptions.main import AlreadyExistsError
from persyval.models.contact import Contact

if TYPE_CHECKING:
    from persyval.services.data_storage.data_storage import DataStorage


def contact_add(
    data_storage: DataStorage,
    contact: Contact,
) -> Contact:
    if contact.uid in data_storage.data.contacts:
        msg = f"{Contact.get_meta_info().singular_name} with uid {contact.uid} already exists."
        raise AlreadyExistsError(msg)

    with data_storage.autosave():
        data_storage.data.contacts[contact.uid] = contact

    return contact
