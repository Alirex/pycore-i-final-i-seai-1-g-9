import enum
from typing import Final


@enum.unique
class Command(enum.StrEnum):
    HELLO = "hello"

    CONTACTS_ROOT = "contacts"

    CONTACTS_LIST = "contacts_list"
    CONTACT_ADD = "contact_add"

    CONTACT_EDIT = "contact_edit"
    CONTACT_VIEW = "contact_view"
    CONTACT_DELETE = "contact_delete"

    CONTACTS_GET_UPCOMING_BIRTHDAYS = "contacts_get_upcoming_birthdays"

    NOTES = "notes"

    STORAGE_ROOT = "storage"

    STORAGE_STATS = "storage_stats"
    STORAGE_CLEAR = "storage_clear"

    HELP = "help"

    EXIT = "exit"

    @classmethod
    def get_default(cls) -> Command:
        return cls.HELP


COMMANDS_ORDER: Final[list[Command]] = [
    Command.HELLO,
    #
    Command.CONTACTS_ROOT,
    #
    Command.CONTACTS_LIST,
    Command.CONTACT_ADD,
    #
    Command.CONTACT_EDIT,
    Command.CONTACT_VIEW,
    Command.CONTACT_DELETE,
    #
    Command.CONTACTS_GET_UPCOMING_BIRTHDAYS,
    #
    Command.NOTES,
    #
    Command.STORAGE_ROOT,
    #
    Command.STORAGE_STATS,
    Command.STORAGE_CLEAR,
    #
    Command.HELP,
    #
    Command.EXIT,
]
"""List of commands in order to display it in different views."""
