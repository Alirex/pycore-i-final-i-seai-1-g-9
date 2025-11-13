from persyval.services.commands.command_meta import CommandMeta
from persyval.services.commands.commands_enum import Command
from persyval.services.handlers.contact_add import CONTACT_ADD_I_ARGS_CONFIG, ContactAddIHandler
from persyval.services.handlers.contact_delete import CONTACT_REMOVE_I_ARGS_CONFIG, ContactDeleteIHandler
from persyval.services.handlers.contacts_list import CONTACT_LIST_I_ARGS_CONFIG, ContactsListIHandler
from persyval.services.handlers.exit import EXIT_I_ARGS_CONFIG, ExitIHandler
from persyval.services.handlers.help import HelpIHandler
from persyval.services.handlers.note_add import NOTE_ADD_I_ARGS_CONFIG, NoteAddIHandler
from persyval.services.handlers.note_delete import NOTE_DELETE_I_ARGS_CONFIG, NoteDeleteIHandler
from persyval.services.handlers.storage_clear import STORAGE_CLEAR_I_ARGS_CONFIG, StorageClearIHandler
from persyval.services.handlers.storage_show_birthdays import (
    STORAGE_SHOW_BIRTHDAYS_I_ARGS_CONFIG,
    StorageShowBirthdaysIHandler,
)
from persyval.services.handlers.storage_stats import StorageStatsIHandler

COMMANDS_META_REGISTRY: dict[Command, CommandMeta] = {
    item.command: item
    for item in [
        CommandMeta(
            command=Command.CONTACT_ADD,
            args_config=CONTACT_ADD_I_ARGS_CONFIG,
            description="Add a contact.",
            handler=ContactAddIHandler,
        ),
        CommandMeta(
            command=Command.CONTACTS_LIST,
            args_config=CONTACT_LIST_I_ARGS_CONFIG,
            description="List contacts. With filtering and actions on the selected contact.",
            handler=ContactsListIHandler,
        ),
        CommandMeta(
            command=Command.CONTACT_DELETE,
            args_config=CONTACT_REMOVE_I_ARGS_CONFIG,
            description="Remove a contact.",
            handler=ContactDeleteIHandler,
        ),
        CommandMeta(
            command=Command.NOTE_ADD,
            args_config=NOTE_ADD_I_ARGS_CONFIG,
            description="Add a note.",
            handler=NoteAddIHandler,
        ),
        CommandMeta(
            command=Command.NOTE_DELETE,
            args_config=NOTE_DELETE_I_ARGS_CONFIG,
            description="Delete a note.",
            handler=NoteDeleteIHandler,
        ),
        CommandMeta(
            command=Command.STORAGE_STATS,
            description="Display statistics about the storage.",
            handler=StorageStatsIHandler,
        ),
        CommandMeta(
            command=Command.STORAGE_CLEAR,
            args_config=STORAGE_CLEAR_I_ARGS_CONFIG,
            description="Clear the storage.",
            handler=StorageClearIHandler,
        ),
        CommandMeta(
            command=Command.STORAGE_SHOW_BIRTHDAYS,
            args_config=STORAGE_SHOW_BIRTHDAYS_I_ARGS_CONFIG,
            description="Show upcomming birthdays from the contacts book.",
            handler=StorageShowBirthdaysIHandler,
        ),
        #
        CommandMeta(
            command=Command.HELP,
            description="Display help information.",
            handler=HelpIHandler,
        ),
        CommandMeta(
            command=Command.EXIT,
            args_config=EXIT_I_ARGS_CONFIG,
            description="Exit the personal assistant chat.",
            handler=ExitIHandler,
        ),
    ]
}
