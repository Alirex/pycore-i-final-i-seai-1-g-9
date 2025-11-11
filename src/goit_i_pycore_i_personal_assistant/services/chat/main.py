from prompt_toolkit import PromptSession
from rich.console import Console

from goit_i_pycore_i_personal_assistant.exceptions.invalid_command_error import InvalidCommandError
from goit_i_pycore_i_personal_assistant.services.commands.commands_meta_registry import COMMANDS_META_REGISTRY
from goit_i_pycore_i_personal_assistant.services.console.completer import get_completer
from goit_i_pycore_i_personal_assistant.services.data_storage.data_storage import DataStorage
from goit_i_pycore_i_personal_assistant.services.get_paths.get_app_dirs import get_data_dir_in_user_space
from goit_i_pycore_i_personal_assistant.services.parse_input.parse_input import parse_input
from goit_i_pycore_i_personal_assistant.utils.format import format_error, format_prompt_message, format_system_message


def main_chat(
    *,
    show_commands: bool = False,
) -> None:
    with DataStorage.load(dir_path=get_data_dir_in_user_space()) as data_storage:
        console = Console()
        prompt_session: PromptSession = PromptSession()  # type: ignore[type-arg]

        msg_intro = format_system_message("Welcome to the personal assistant chat.")
        console.print(msg_intro)

        while True:
            input_prompt_msg = format_prompt_message("Enter command: ")
            console.print(input_prompt_msg)

            user_input = prompt_session.prompt(
                message="> ",
                completer=get_completer(),
            )

            try:
                parsed_input = parse_input(user_input)
            except InvalidCommandError as exc:
                msg_error = format_error("Invalid Command", str(exc))
                console.print(msg_error)
                continue

            if show_commands:
                console.print(parsed_input.get_rich_cli())

            command_meta = COMMANDS_META_REGISTRY[parsed_input.command]

            handler_obj = command_meta.handler(
                args=parsed_input.args,
                #
                data_storage=data_storage,
                #
                console=console,
            )
            handler_output = handler_obj.run()

            if handler_output.message_rich:
                console.print(handler_output.message_rich)

            if handler_output.is_exit:
                break
