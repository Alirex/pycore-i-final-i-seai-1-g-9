import pathlib  # noqa: TC003
from typing import Annotated

import rich.console
import typer

from persyval.cli.chat.main import get_storage_dir_fact
from persyval.services.data_storage_filler.data_storage_filler import (
    fill_data_storage_by_path,
)
from persyval.services.get_paths.get_app_dirs import (
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


@app.command()
def fill_storage(
    *,
    amount: Annotated[
        int,
        typer.Option(
            help="Amount of entities for each type to be added.",
        ),
    ] = 10,
    storage_dir: Annotated[
        pathlib.Path | None,
        typer.Option(
            help="Storage directory.",
        ),
    ] = None,
    init_only: Annotated[
        bool,
        typer.Option(
            "--init-only",
            help="Only add data in section, if it doesn't exist.",
        ),
    ] = False,
) -> None:
    """Fill the storage with some data."""
    fill_data_storage_by_path(
        storage_dir=get_storage_dir_fact(
            no_persistence=False,
            storage_dir_external=storage_dir,
        ),
        amount=amount,
        init_only=init_only,
    )


@app.command()
def debug() -> None:
    """Debug the application."""
    print("debug")
