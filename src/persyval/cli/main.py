import typer

from persyval.cli.chat.main import app as app_chat
from persyval.cli.helpers.main import app as app_helpers

app = typer.Typer(
    pretty_exceptions_enable=False,
    pretty_exceptions_show_locals=False,
)

app.add_typer(app_chat, name="chat")
app.add_typer(app_helpers, name="helpers")
