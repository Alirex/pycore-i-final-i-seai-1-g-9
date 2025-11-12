import enum
from typing import Final


@enum.unique
class Command(enum.StrEnum):
    CONTACT_ADD = "contact_add"
    CONTACT_LIST = "contact_list"
    CONTACT_DELETE = "contact_delete"

    NOTE_ADD = "note_add"
    # NOTE_DELETE = "note_delete"

    STORAGE_STATS = "storage_stats"
    STORAGE_CLEAR = "storage_clear"

    HELP = "help"

    EXIT = "exit"

    @classmethod
    def get_default(cls) -> Command:
        return cls.HELP


COMMANDS_ORDER: Final[list[Command]] = [
    Command.CONTACT_ADD,
    Command.CONTACT_LIST,
    Command.CONTACT_DELETE,
    #
    Command.NOTE_ADD,
    # Command.NOTE_DELETE,
    # #
    Command.STORAGE_STATS,
    Command.STORAGE_CLEAR,
    #
    Command.HELP,
    #
    Command.EXIT,
]
"""List of commands in order to display it in different views."""
