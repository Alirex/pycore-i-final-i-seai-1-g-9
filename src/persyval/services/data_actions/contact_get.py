from typing import TYPE_CHECKING

from persyval.exceptions.main import NotFoundError

if TYPE_CHECKING:
    from persyval.models.contact import Contact, ContactUid
    from persyval.services.data_storage.data_storage import DataStorage


def contact_get(
    data_storage: DataStorage,
    contact_uid: ContactUid,
) -> Contact:
    try:
        return data_storage.data.contacts[contact_uid]
    except KeyError as exc:
        msg = f"Contact with uid {contact_uid} not found."
        raise NotFoundError(msg) from exc
