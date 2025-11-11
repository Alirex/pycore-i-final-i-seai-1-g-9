import rich.console
import typer

from goit_i_pycore_i_personal_assistant.services.get_paths.get_app_dirs import (
    get_app_dirs_in_user_space,
)

app = typer.Typer()


@app.command()
def show_paths() -> None:
    """Show the paths that used for storage."""
    console = rich.console.Console()
    console.print(get_app_dirs_in_user_space().get_for_cli())


@app.command()
def clear_storage() -> None:
    """Clear all stored data."""
    get_app_dirs_in_user_space().remove_all()

    console = rich.console.Console()
    console.print("All stored data has been cleared.")
