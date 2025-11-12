import typer

from persyval.services.chat.main import main_chat

app = typer.Typer()


@app.command()
def run(
    *,
    show_commands: bool = False,
    hide_intro: bool = False,
    non_interactive: bool = False,
    plain_render: bool = False,
    predefined_input: str | None = None,
) -> None:
    """Run the personal assistant chat.

    Provides interactive chat with the personal assistant.

    Also, can be used as a command line tool.
    """
    main_chat(
        show_commands=show_commands,
        hide_intro=hide_intro,
        non_interactive=non_interactive,
        plain_render=plain_render,
        predefined_input=predefined_input,
    )
