import pathlib  # noqa: TC003
from typing import Annotated, Final

import environs
import typer

from persyval.cli.constants import CLI_DOC_NEWLINE, CLI_DOC_NEWLINE_AT_END
from persyval.services.chat.main import main_chat
from persyval.services.get_paths.get_app_dirs import get_data_dir_in_user_space

app = typer.Typer()

ENV_VAR_NAME_I_PREDEFINED_INPUT: Final[str] = "PERSYVAL_I_PREDEFINED_INPUT"

ENV_VAR_NAME_I_NO_PERSISTENCE: Final[str] = "PERSYVAL_I_NO_PERSISTENCE"


@app.command()
def run(  # noqa: PLR0913
    *,
    predefined_input: Annotated[
        str | None,
        typer.Argument(
            help=f"Predefined input to be used instead of prompting the user. {CLI_DOC_NEWLINE}"
            "Useful for testing and automation purposes. "
            f"Related env var: '{ENV_VAR_NAME_I_PREDEFINED_INPUT}' {CLI_DOC_NEWLINE_AT_END}",
        ),
    ] = None,
    #
    show_commands: Annotated[
        bool,
        typer.Option(
            "--show-commands",
            help=f"Show input commands. {CLI_DOC_NEWLINE}Useful for debugging purposes.{CLI_DOC_NEWLINE_AT_END}",
        ),
    ] = False,
    hide_intro: Annotated[
        bool,
        typer.Option("--hide-intro", help=f"Hide the introduction message.{CLI_DOC_NEWLINE_AT_END}"),
    ] = False,
    #
    non_interactive: Annotated[
        bool,
        typer.Option(
            "--non-interactive",
            help=f"Run in non-interactive mode. {CLI_DOC_NEWLINE}"
            f"Do not prompt for user input. Exit after completion of action.{CLI_DOC_NEWLINE_AT_END}",
        ),
    ] = False,
    plain_render: Annotated[
        bool,
        typer.Option(
            "--plain-render",
            help=f"Render plain text without any special formatting (e.g., colors, styles). {CLI_DOC_NEWLINE}"
            f"Useful for simple terminals and CLI automations scripts.{CLI_DOC_NEWLINE_AT_END}",
        ),
    ] = False,
    terminal_simplified: Annotated[
        bool,
        typer.Option(
            "--terminal-simplified",
            help=f"Use simplified terminal input. {CLI_DOC_NEWLINE}"
            "Useful for testing and automation purposes. "
            f"Also, useful for some debugging tools.{CLI_DOC_NEWLINE_AT_END}",
        ),
    ] = False,
    raise_sys_exit_on_error: Annotated[
        bool,
        typer.Option(
            "--raise-sys-exit-on-error",
            help=f"Raise sys.exit(1) on error. {CLI_DOC_NEWLINE}"
            f"Useful for testing and automation purposes.{CLI_DOC_NEWLINE_AT_END}",
        ),
    ] = False,
    #
    storage_dir: Annotated[
        pathlib.Path | None,
        typer.Option(
            help=f"Storage directory. {CLI_DOC_NEWLINE} "
            f"Use env var '{ENV_VAR_NAME_I_NO_PERSISTENCE}' if you want to disable storing data to the file system. "
            f"{CLI_DOC_NEWLINE_AT_END}",
        ),
    ] = None,
    #
    use_advanced_completer: Annotated[
        bool,
        typer.Option(
            "--use-advanced-completer",
            help=f"Use advanced completer. {CLI_DOC_NEWLINE} "
            f"Useful if you need to use advanced commands.{CLI_DOC_NEWLINE_AT_END}",
        ),
    ] = False,
) -> None:
    """Run the personal assistant chat.

    Provides interactive chat with the personal assistant.

    Also, it can be used as a command line tool.
    """
    environs.env.read_env()

    persyval_i_predefined_input = environs.env.str(ENV_VAR_NAME_I_PREDEFINED_INPUT, "")

    predefined_input = predefined_input or persyval_i_predefined_input or None

    # TODO: (?) Add check for some terminal types. Like `dumb`, etc.
    term = environs.env.str("TERM", "")
    terminal_simplified = terminal_simplified or (not term)

    persyval_i_no_persistence = environs.env.bool(ENV_VAR_NAME_I_NO_PERSISTENCE, False)

    get_data_dir_in_user_space()
    if persyval_i_no_persistence:
        storage_dir_fact = None
    elif storage_dir is None:
        storage_dir_fact = get_data_dir_in_user_space()
    else:
        storage_dir_fact = storage_dir

    main_chat(
        show_commands=show_commands,
        hide_intro=hide_intro,
        #
        non_interactive=non_interactive,
        plain_render=plain_render,
        terminal_simplified=terminal_simplified,
        raise_sys_exit_on_error=raise_sys_exit_on_error,
        #
        predefined_input=predefined_input,
        #
        storage_dir=storage_dir_fact,
        #
        use_advanced_completer=use_advanced_completer,
    )
