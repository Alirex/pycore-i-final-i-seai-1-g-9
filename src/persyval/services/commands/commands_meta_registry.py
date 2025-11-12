from persyval.services.commands.command_meta import ArgMetaConfig, ArgType, CommandMeta
from persyval.services.commands.commands_enum import Command
from persyval.services.handlers.contact_add import ContactAddIHandler
from persyval.services.handlers.contact_list import ContactListIHandler
from persyval.services.handlers.exit import ExitIHandler
from persyval.services.handlers.help import HelpIHandler
from persyval.services.handlers.storage_clear import StorageClearIHandler
from persyval.services.handlers.storage_stats import StorageStatsIHandler

COMMANDS_META_REGISTRY: dict[Command, CommandMeta] = {
    item.command: item
    for item in [
        CommandMeta(
            command=Command.CONTACT_ADD,
            description="Add a contact.",
            handler=ContactAddIHandler,
        ),
        CommandMeta(
            command=Command.CONTACT_LIST,
            description="List contacts. With filtering and actions on the selected contact.",
            handler=ContactListIHandler,
        ),
        #
        CommandMeta(
            command=Command.STORAGE_STATS,
            description="Display statistics about the storage.",
            handler=StorageStatsIHandler,
        ),
        CommandMeta(
            command=Command.STORAGE_CLEAR,
            args=[
                ArgMetaConfig(
                    name="force",
                    type_=ArgType.BOOL,
                ),
            ],
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
            args=[
                ArgMetaConfig(
                    name="force",
                    type_=ArgType.BOOL,
                ),
            ],
            description="Exit the personal assistant chat.",
            handler=ExitIHandler,
        ),
    ]
}
