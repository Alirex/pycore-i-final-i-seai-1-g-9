from persyval.services.commands.command_meta import CommandMeta
from persyval.services.commands.commands_enum import Command
from persyval.services.handlers.contact_add import ContactAddIHandler
from persyval.services.handlers.contact_list import ContactListIHandler
from persyval.services.handlers.exit import ExitIHandler
from persyval.services.handlers.help import HelpIHandler

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
            description="List contacts.",
            handler=ContactListIHandler,
        ),
        #
        CommandMeta(
            command=Command.HELP,
            description="Display help information.",
            handler=HelpIHandler,
        ),
        CommandMeta(
            command=Command.EXIT,
            description="Exit the personal assistant chat.",
            handler=ExitIHandler,
        ),
    ]
}
