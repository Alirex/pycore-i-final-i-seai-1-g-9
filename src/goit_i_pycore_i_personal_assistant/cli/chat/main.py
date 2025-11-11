import typer

from goit_i_pycore_i_personal_assistant.services.chat.main import main_chat

app = typer.Typer()


@app.command()
def run(
    *,
    show_commands: bool = False,
) -> None:
    """Run the personal assistant chat.

    Provides interactive chat with the personal assistant.
    """
    main_chat(show_commands=show_commands)
