import uuid
from typing import Annotated, NewType

from pydantic import AfterValidator, BaseModel

PhoneUid = NewType("PhoneUid", uuid.UUID)


def phone_validator(phone: str) -> str:
    # TODO: validate phone number
    return phone


class Phone(BaseModel):
    number: Annotated[str, AfterValidator(phone_validator)]
