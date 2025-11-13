import enum
from typing import Final


@enum.unique
class Command(enum.StrEnum):
    CONTACTS_LIST = "contacts_list"
    CONTACT_ADD = "contact_add"
    CONTACT_DELETE = "contact_delete"
    CONTACTS_GET_UPCOMING_BIRTHDAYS = "contacts_get_upcoming_birthdays"

    NOTE_ADD = "note_add"
    NOTE_DELETE = "note_delete"
    NOTE_LIST = "note_list"

    STORAGE_STATS = "storage_stats"
    STORAGE_CLEAR = "storage_clear"

    HELP = "help"

    EXIT = "exit"

    @classmethod
    def get_default(cls) -> Command:
        return cls.HELP


COMMANDS_ORDER: Final[list[Command]] = [
    Command.CONTACTS_LIST,
    Command.CONTACT_ADD,
    Command.CONTACT_DELETE,
    Command.CONTACTS_GET_UPCOMING_BIRTHDAYS,
    #
    Command.NOTE_ADD,
    Command.NOTE_DELETE,
    Command.NOTE_LIST,
    # #
    Command.STORAGE_STATS,
    Command.STORAGE_CLEAR,
    #
    Command.HELP,
    #
    Command.EXIT,
]
"""List of commands in order to display it in different views."""
