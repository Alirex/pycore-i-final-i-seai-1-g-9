from persyval.services.commands.command_meta import CommandMeta
from persyval.services.commands.commands_enum import Command
from persyval.services.handlers.exit import ExitIHandler
from persyval.services.handlers.help import HelpIHandler

COMMANDS_META_REGISTRY: dict[Command, CommandMeta] = {
    item.command: item
    for item in [
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
