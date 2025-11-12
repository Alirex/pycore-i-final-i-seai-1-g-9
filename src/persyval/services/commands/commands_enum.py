import enum
from typing import Final


@enum.unique
class Command(enum.StrEnum):
    CONTACT_ADD = "contact_add"
    CONTACT_LIST = "contact_list"

    # NOTE_ADD = "note_add"
    # NOTE_REMOVE = "note_remove"
    #
    # CLEAR_STORAGE = "clear_storage"

    HELP = "help"

    EXIT = "exit"

    @classmethod
    def get_default(cls) -> Command:
        return cls.HELP


COMMANDS_ORDER: Final[list[Command]] = [
    Command.CONTACT_ADD,
    Command.CONTACT_LIST,
    # Command.NOTE_ADD,
    # Command.NOTE_REMOVE,
    # #
    # Command.CLEAR_STORAGE,
    #
    Command.HELP,
    #
    Command.EXIT,
]
"""List of commands in order to display it in different views."""
