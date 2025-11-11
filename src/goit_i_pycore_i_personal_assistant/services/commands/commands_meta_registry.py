from goit_i_pycore_i_personal_assistant.services.commands.command_meta import CommandMeta
from goit_i_pycore_i_personal_assistant.services.commands.commands_enum import Command
from goit_i_pycore_i_personal_assistant.services.handlers.exit import ExitIHandler
from goit_i_pycore_i_personal_assistant.services.handlers.help import HelpIHandler

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
