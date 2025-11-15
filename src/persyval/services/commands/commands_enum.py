import enum
from typing import Final


@enum.unique
class Command(enum.StrEnum):
    HELLO = "hello"

    ROOT = "root"

    # [contacts]-[BEGIN]
    CONTACTS_ROOT = "contacts"

    CONTACTS_LIST = "contacts_list"
    CONTACT_ADD = "contact_add"
    CONTACTS_EXPORT = "contacts_export"

    CONTACT_EDIT = "contact_edit"
    CONTACT_VIEW = "contact_view"
    CONTACT_DELETE = "contact_delete"

    CONTACTS_GET_UPCOMING_BIRTHDAYS = "contacts_get_upcoming_birthdays"
    # [contacts]-[END]

    # [notes]-[BEGIN]
    NOTES_ROOT = "notes"

    NOTES_LIST = "notes_list"
    NOTE_ADD = "note_add"

    NOTE_EDIT = "note_edit"
    NOTE_VIEW = "note_view"
    NOTE_DELETE = "note_delete"

    # [notes]-[END]

    # [storage]-[BEGIN]
    STORAGE_ROOT = "storage"

    STORAGE_STATS = "storage_stats"
    STORAGE_CLEAR = "storage_clear"
    # [storage]-[END]

    HELP = "help"

    EXIT = "exit"

    @classmethod
    def get_default(cls) -> Command:
        return cls.ROOT


COMMANDS_ORDER: Final[list[Command]] = [
    Command.ROOT,
    #
    Command.HELLO,
    #
    # [contacts]-[BEGIN]
    Command.CONTACTS_ROOT,
    #
    Command.CONTACTS_LIST,
    Command.CONTACT_ADD,
    Command.CONTACTS_EXPORT,
    #
    Command.CONTACT_EDIT,
    Command.CONTACT_VIEW,
    Command.CONTACT_DELETE,
    #
    Command.CONTACTS_GET_UPCOMING_BIRTHDAYS,
    # [contacts]-[END]
    #
    # [notes]-[BEGIN]
    Command.NOTES_ROOT,
    #
    Command.NOTES_LIST,
    Command.NOTE_ADD,
    #
    Command.NOTE_EDIT,
    Command.NOTE_VIEW,
    Command.NOTE_DELETE,
    # [notes]-[END]
    #
    # [storage]-[BEGIN]
    Command.STORAGE_ROOT,
    #
    Command.STORAGE_STATS,
    Command.STORAGE_CLEAR,
    # [storage]-[END]
    #
    Command.HELP,
    #
    Command.EXIT,
]
"""List of commands in order to display it in different views."""
