from typing import TYPE_CHECKING

from persyval.exceptions.main import NotFoundError

if TYPE_CHECKING:
    from persyval.models.contact import ContactUid
    from persyval.services.data_storage.data_storage import DataStorage


def contact_delete(
    data_storage: DataStorage,
    contact_uid: ContactUid,
) -> None:
    try:
        with data_storage.autosave():
            del data_storage.data.contacts[contact_uid]
    except KeyError as exc:
        msg = f"Contact with uid {contact_uid} not found."
        raise NotFoundError(msg) from exc
