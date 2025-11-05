import typer

app = typer.Typer()


@app.command()
def run() -> None:
    """Run the personal assistant chat.

    Provides interactive chat with the personal assistant.
    """
    typer.echo("Hello World!")
