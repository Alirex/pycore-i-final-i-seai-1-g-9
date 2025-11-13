from typing import Annotated, Final

import environs
import typer

from persyval.cli.constants import CLI_DOC_NEWLINE, CLI_DOC_NEWLINE_AT_END
from persyval.services.chat.main import main_chat

app = typer.Typer()

ENV_VAR_NAME_I_PREDEFINED_INPUT: Final[str] = "PERSYVAL_I_PREDEFINED_INPUT"


@app.command()
def run(  # noqa: PLR0913
    *,
    predefined_input: Annotated[
        str | None,
        typer.Argument(
            help=f"Predefined input to be used instead of prompting the user. {CLI_DOC_NEWLINE}"
            "Useful for testing and automation purposes. "
            f"Related env: '{ENV_VAR_NAME_I_PREDEFINED_INPUT}' {CLI_DOC_NEWLINE_AT_END}",
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
    #
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

    main_chat(
        show_commands=show_commands,
        hide_intro=hide_intro,
        non_interactive=non_interactive,
        plain_render=plain_render,
        terminal_simplified=terminal_simplified,
        predefined_input=predefined_input,
    )
