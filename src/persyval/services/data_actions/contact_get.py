from typing import TYPE_CHECKING

from persyval.exceptions.main import NotFoundError
from persyval.models.contact import Contact

if TYPE_CHECKING:
    from persyval.models.contact import ContactUid
    from persyval.services.data_storage.data_storage import DataStorage


def contact_get(
    data_storage: DataStorage,
    uid: ContactUid,
) -> Contact:
    try:
        return data_storage.data.contacts[uid]
    except KeyError as exc:
        msg = f"{Contact.get_meta_info().singular_name} with uid {uid} not found."
        raise NotFoundError(msg) from exc
