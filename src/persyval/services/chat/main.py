from prompt_toolkit import PromptSession
from rich.console import Console

from persyval.services.chat.get_input import get_input
from persyval.services.chat.parse_input_and_make_action import LoopAction, parse_input_and_make_action
from persyval.services.data_storage.data_storage import DataStorage
from persyval.services.get_paths.get_app_dirs import get_data_dir_in_user_space
from persyval.services.intro.render_intro import render_intro

# TODO: (?) Group some args to class


def main_chat(  # noqa: PLR0913
    *,
    show_commands: bool = False,
    hide_intro: bool = False,
    #
    non_interactive: bool = False,
    plain_render: bool = False,
    terminal_simplified: bool = False,
    #
    predefined_input: str | None = None,
) -> None:
    with DataStorage.load(dir_path=get_data_dir_in_user_space()) as data_storage:
        console = Console()
        prompt_session: PromptSession = PromptSession()  # type: ignore[type-arg]

        if not hide_intro:
            render_intro(console)

        while True:
            user_input = predefined_input or get_input(console=console, prompt_session=prompt_session)

            loop_action = parse_input_and_make_action(
                console=console,
                data_storage=data_storage,
                #
                user_input=user_input,
                show_commands=show_commands,
                #
                non_interactive=non_interactive,
                plain_render=plain_render,
                terminal_simplified=terminal_simplified,
            )

            if non_interactive:
                break

            match loop_action:
                case LoopAction.EXIT:
                    break
                case _:
                    continue
