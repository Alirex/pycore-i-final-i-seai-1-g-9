from typing import Final

import phonenumbers

from persyval.exceptions.main import InvalidDataError

DEFAULT_REGION: Final[str] = "UA"


def parse_phones(phones: str) -> list[str]:
    return list(filter(None, phones.split(",")))


def validate_phone(phone: str) -> str:
    user_phone = phone.strip()
    if not user_phone:
        msg = f"Phone number is empty: {phone}"
        raise InvalidDataError(msg)

    try:
        if user_phone.startswith("+"):
            parsed = phonenumbers.parse(user_phone, None)
        else:
            parsed = phonenumbers.parse(user_phone, DEFAULT_REGION)
    except phonenumbers.NumberParseException as e:
        msg = f"Invalid phone number format: {user_phone}"
        raise InvalidDataError(msg) from e

    if not phonenumbers.is_valid_number(parsed):
        msg = f"Invalid phone number: {user_phone}"
        raise InvalidDataError(msg)

    # Note: This will break the search on the phone number. Maybe use this in display mode.
    # return phonenumbers.format_number(
    #     parsed,
    #     phonenumbers.PhoneNumberFormat.E164,
    # )

    return user_phone


def validate_phone_list(phones: list[str]) -> list[str]:
    validated_phones = []

    for phone in phones:
        validated = validate_phone(phone)
        validated_phones.append(validated)

    # Remove duplicates. But keep the order.
    existing_phones = set()
    unique_phones = []
    for phone in validated_phones:
        if phone not in existing_phones:
            unique_phones.append(phone)
            existing_phones.add(phone)

    return unique_phones
