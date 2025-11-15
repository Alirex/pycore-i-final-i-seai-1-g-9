from typing import TYPE_CHECKING

from persyval.exceptions.main import NotFoundError
from persyval.models.contact import Contact

if TYPE_CHECKING:
    from persyval.models.contact import ContactUid
    from persyval.services.data_storage.data_storage import DataStorage


def contact_delete(
    data_storage: DataStorage,
    contact_uid: ContactUid,
) -> Contact:
    try:
        with data_storage.autosave():
            contact = data_storage.data.contacts.pop(contact_uid)
    except KeyError as exc:
        msg = f"{Contact.get_meta_info().singular_name} with uid {contact_uid} not found."
        raise NotFoundError(msg) from exc

    return contact
