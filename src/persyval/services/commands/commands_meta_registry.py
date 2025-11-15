from persyval.models.contact import Contact
from persyval.models.note import Note
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
    CONTACTS_LIST_I_ARGS_CONFIG,
    ContactsListIHandler,
)
from persyval.services.handlers.contacts_root import (
    CONTACTS_ROOT_I_ARGS_CONFIG,
    ContactsRootIHandler,
)
from persyval.services.handlers.exit import EXIT_I_ARGS_CONFIG, ExitIHandler
from persyval.services.handlers.hello import HelloIHandler
from persyval.services.handlers.help import HELP_I_ARGS_CONFIG, HelpIHandler
from persyval.services.handlers.note_delete import NOTE_DELETE_I_ARGS_CONFIG, NoteDeleteIHandler
from persyval.services.handlers.note_view import (
    NOTE_VIEW_I_ARGS_CONFIG,
    NoteViewIHandler,
)
from persyval.services.handlers.notes_list import NOTES_I_ARGS_CONFIG_LIST_I_ARGS_CONFIG, NotesListIHandler
from persyval.services.handlers.root import RootIHandler
from persyval.services.handlers.shared.args_i_empty import ARGS_CONFIG_I_EMPTY
from persyval.services.handlers.storage_clear import (
    STORAGE_CLEAR_I_ARGS_CONFIG,
    StorageClearIHandler,
)
from persyval.services.handlers.storage_root import (
    STORAGE_ROOT_I_ARGS_CONFIG,
    StorageRootIHandler,
)
from persyval.services.handlers.storage_stats import StorageStatsIHandler

COMMANDS_META_REGISTRY: dict[Command, CommandMeta] = {
    item.command: item
    for item in [
        CommandMeta(
            command=Command.HELLO,
            args_config=ARGS_CONFIG_I_EMPTY,
            description="Display greeting.",
            handler=HelloIHandler,
        ),
        CommandMeta(
            command=Command.ROOT,
            args_config=ARGS_CONFIG_I_EMPTY,
            description="Display root menu.",
            handler=RootIHandler,
            hidden=True,
        ),
        #
        CommandMeta(
            command=Command.CONTACTS_ROOT,
            args_config=CONTACTS_ROOT_I_ARGS_CONFIG,
            description=f"Manage {Contact.get_meta_info().singular_name}.",
            handler=ContactsRootIHandler,
        ),
        #
        CommandMeta(
            command=Command.CONTACTS_LIST,
            args_config=CONTACTS_LIST_I_ARGS_CONFIG,
            description=f"List {Contact.get_meta_info().plural_name}. "
            f"With filtering and actions on the selected {Contact.get_meta_info().plural_name}.",
            handler=ContactsListIHandler,
            hidden=True,
        ),
        CommandMeta(
            command=Command.CONTACT_ADD,
            args_config=CONTACT_ADD_I_ARGS_CONFIG,
            description=f"Add a {Contact.get_meta_info().singular_name}.",
            handler=ContactAddIHandler,
            hidden=True,
        ),
        #
        CommandMeta(
            command=Command.CONTACT_EDIT,
            args_config=CONTACT_EDIT_I_ARGS_CONFIG,
            description=f"Edit a {Contact.get_meta_info().singular_name}.",
            handler=ContactEditIHandler,
            hidden=True,
        ),
        CommandMeta(
            command=Command.CONTACT_VIEW,
            args_config=CONTACT_VIEW_I_ARGS_CONFIG,
            description=f"View a {Contact.get_meta_info().singular_name}.",
            handler=ContactViewIHandler,
            hidden=True,
        ),
        CommandMeta(
            command=Command.CONTACT_DELETE,
            args_config=CONTACT_DELETE_I_ARGS_CONFIG,
            description=f"Delete a {Contact.get_meta_info().singular_name}.",
            handler=ContactDeleteIHandler,
            hidden=True,
        ),
        #
        CommandMeta(
            command=Command.CONTACTS_GET_UPCOMING_BIRTHDAYS,
            args_config=CONTACTS_GET_BIRTHDAYS_I_ARGS_CONFIG,
            description=f"Show upcoming birthdays for the {Contact.get_meta_info().plural_name}.",
            handler=ContactsGetUpcomingBirthdaysIHandler,
            hidden=True,
        ),
        #
        CommandMeta(
            command=Command.NOTES_LIST,
            args_config=NOTES_I_ARGS_CONFIG_LIST_I_ARGS_CONFIG,
            description=f"List {Note.get_meta_info().plural_name}. "
            f"With filtering and actions on the selected {Note.get_meta_info().plural_name}.",
            handler=NotesListIHandler,
        ),
        #
        CommandMeta(
            command=Command.NOTE_VIEW,
            args_config=NOTE_VIEW_I_ARGS_CONFIG,
            description=f"View a {Note.get_meta_info().singular_name}.",
            handler=NoteViewIHandler,
            hidden=True,
        ),
        CommandMeta(
            command=Command.NOTE_DELETE,
            args_config=NOTE_DELETE_I_ARGS_CONFIG,
            description=f"Delete a {Note.get_meta_info().singular_name}.",
            handler=NoteDeleteIHandler,
            hidden=True,
        ),
        #
        CommandMeta(
            command=Command.STORAGE_ROOT,
            args_config=STORAGE_ROOT_I_ARGS_CONFIG,
            description="Manage storage.",
            handler=StorageRootIHandler,
        ),
        #
        CommandMeta(
            command=Command.STORAGE_STATS,
            args_config=ARGS_CONFIG_I_EMPTY,
            description="Display statistics about the storage.",
            handler=StorageStatsIHandler,
            hidden=True,
        ),
        CommandMeta(
            command=Command.STORAGE_CLEAR,
            args_config=STORAGE_CLEAR_I_ARGS_CONFIG,
            description="Clear the storage.",
            handler=StorageClearIHandler,
            hidden=True,
        ),
        #
        CommandMeta(
            command=Command.HELP,
            args_config=HELP_I_ARGS_CONFIG,
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
