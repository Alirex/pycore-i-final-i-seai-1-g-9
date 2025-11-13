from typing import Annotated, Final

import environs
import typer

from persyval.services.chat.main import main_chat

app = typer.Typer()

ENV_VAR_NAME_I_PREDEFINED_INPUT: Final[str] = "PERSYVAL_I_PREDEFINED_INPUT"


@app.command()
def run(  # noqa: PLR0913
    *,
    show_commands: Annotated[
        bool,
        typer.Option(help="Show input commands. \n\nUseful for debugging purposes.\n\n."),
    ] = False,
    hide_intro: Annotated[
        bool,
        typer.Option(help="Hide the introduction message.\n\n."),
    ] = False,
    #
    non_interactive: Annotated[
        bool,
        typer.Option(
            help="Run in non-interactive mode. \n\nDo not prompt for user input. Exit after completion of action.\n\n.",
        ),
    ] = False,
    plain_render: Annotated[
        bool,
        typer.Option(
            help="Render plain text without any special formatting (e.g., colors, styles). \n\n"
            "Useful for simple terminals and CLI automations scripts.\n\n.",
        ),
    ] = False,
    terminal_simplified: Annotated[
        bool,
        typer.Option(
            help="Use simplified terminal input. \n\n"
            "Useful for testing and automation purposes. "
            "Also, useful for some debugging tools.\n\n.",
        ),
    ] = False,
    #
    predefined_input: Annotated[
        str | None,
        typer.Option(
            help="Predefined input to be used instead of prompting the user. \n\n"
            "Useful for testing and automation purposes. "
            f"Related env: '{ENV_VAR_NAME_I_PREDEFINED_INPUT}'\n\n.",
        ),
    ] = None,
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
