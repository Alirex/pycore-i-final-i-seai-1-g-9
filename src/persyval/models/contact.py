import datetime
import uuid
from typing import Annotated, NewType

from pydantic import BaseModel, EmailStr, Field

from persyval.models.phone import Phone

ContactName = NewType("ContactName", str)
ContactUid = NewType("ContactUid", uuid.UUID)


class Contact(BaseModel):
    uid: ContactUid = Field(default_factory=lambda: ContactUid(uuid.uuid7()))

    name: Annotated[ContactName, Field(description="The name of the contact.", min_length=1)]

    address: Annotated[str | None, Field(description="The address of the contact.")] = None

    phones: list[Phone] = Field(
        default_factory=list,
        description="List of phone numbers associated with the contact.",
    )

    email: EmailStr

    birthday: datetime.date
