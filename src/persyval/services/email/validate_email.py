from email_validator import EmailNotValidError
from email_validator import validate_email as validate_email_external

from persyval.exceptions.main import EmptyDataError, InvalidDataError


def parse_emails(emails: str) -> list[str]:
    return list(filter(None, emails.split(",")))


def validate_email(email: str) -> str:
    user_email = email.strip()
    if not user_email:
        msg = f"Email address is empty: {email}"
        raise EmptyDataError(msg)

    try:
        valid = validate_email_external(user_email, check_deliverability=False)

    except EmailNotValidError as e:
        msg = f"Invalid email address: {user_email} ({e!s})"
        raise InvalidDataError(msg) from e

    return valid.normalized


def validate_email_list(emails: list[str]) -> list[str]:
    validated_emails: list[str] = []

    for email in emails:
        try:
            validated = validate_email(email)
        except EmptyDataError:
            continue
        validated_emails.append(validated)

    exist: set[str] = set()
    unique_emails: list[str] = []
    for email in validated_emails:
        if email not in exist:
            unique_emails.append(email)
            exist.add(email)

    return unique_emails
