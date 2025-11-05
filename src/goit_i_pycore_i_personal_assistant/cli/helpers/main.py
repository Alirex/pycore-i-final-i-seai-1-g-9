import typer
import rich.console
from goit_i_pycore_i_personal_assistant.services.get_paths.get_app_paths import (
    get_app_paths,
)

app = typer.Typer()


@app.command()
def show_paths() -> None:
    """Show the paths that used for storage."""
    console = rich.console.Console()
    console.print("Paths:")
    console.print(get_app_paths().get_for_cli())


@app.command()
def clear_storage() -> None:
    """Clear all stored data."""
    get_app_paths().remove_all()

    console = rich.console.Console()
    console.print("All stored data has been cleared.")
