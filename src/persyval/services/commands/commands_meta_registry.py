from persyval.services.commands.command_meta import CommandMeta
from persyval.services.commands.commands_enum import Command
from persyval.services.handlers.contact_add import (
    CONTACT_ADD_I_ARGS_CONFIG,
    ContactAddIHandler,
)
from persyval.services.handlers.contact_delete import (
    CONTACT_DELETE_I_ARGS_CONFIG,
    ContactDeleteIHandler,
)
from persyval.services.handlers.contact_edit import (
    CONTACT_EDIT_I_ARGS_CONFIG,
    ContactEditIHandler,
)
from persyval.services.handlers.contact_view import (
    CONTACT_VIEW_I_ARGS_CONFIG,
    ContactViewIHandler,
)
from persyval.services.handlers.contacts_get_upcoming_birthdays import (
    CONTACTS_GET_BIRTHDAYS_I_ARGS_CONFIG,
    ContactsGetUpcomingBirthdaysIHandler,
)
from persyval.services.handlers.contacts_list import (
    CONTACT_LIST_I_ARGS_CONFIG,
    ContactsListIHandler,
)
from persyval.services.handlers.exit import EXIT_I_ARGS_CONFIG, ExitIHandler
from persyval.services.handlers.help import HelpIHandler
from persyval.services.handlers.notes import NOTES_I_ARGS_CONFIG, NotesIHandler
from persyval.services.handlers.storage_clear import (
    STORAGE_CLEAR_I_ARGS_CONFIG,
    StorageClearIHandler,
)
from persyval.services.handlers.storage_stats import StorageStatsIHandler

COMMANDS_META_REGISTRY: dict[Command, CommandMeta] = {
    item.command: item
    for item in [
        CommandMeta(
            command=Command.CONTACTS_LIST,
            args_config=CONTACT_LIST_I_ARGS_CONFIG,
            description="List contacts. With filtering and actions on the selected contact.",
            handler=ContactsListIHandler,
        ),
        CommandMeta(
            command=Command.CONTACT_ADD,
            args_config=CONTACT_ADD_I_ARGS_CONFIG,
            description="Add a contact.",
            handler=ContactAddIHandler,
        ),
        CommandMeta(
            command=Command.CONTACT_EDIT,
            args_config=CONTACT_EDIT_I_ARGS_CONFIG,
            description="Edit a contact.",
            handler=ContactEditIHandler,
        ),
        CommandMeta(
            command=Command.CONTACT_VIEW,
            args_config=CONTACT_VIEW_I_ARGS_CONFIG,
            description="View a contact.",
            handler=ContactViewIHandler,
        ),
        CommandMeta(
            command=Command.CONTACT_DELETE,
            args_config=CONTACT_DELETE_I_ARGS_CONFIG,
            description="Delete a contact.",
            handler=ContactDeleteIHandler,
        ),
        #
        CommandMeta(
            command=Command.CONTACTS_GET_UPCOMING_BIRTHDAYS,
            args_config=CONTACTS_GET_BIRTHDAYS_I_ARGS_CONFIG,
            description="Show upcoming birthdays from the contacts book.",
            handler=ContactsGetUpcomingBirthdaysIHandler,
        ),
        #
        CommandMeta(
            command=Command.NOTES,
            args_config=NOTES_I_ARGS_CONFIG,
            description="Handle operations with notes.",
            handler=NotesIHandler,
        ),
        #
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
