import typer

from goit_i_pycore_i_personal_assistant.cli.chat.main import app as app_chat
from goit_i_pycore_i_personal_assistant.cli.helpers.main import app as app_helpers

app = typer.Typer()
app.add_typer(app_chat, name="chat")
app.add_typer(app_helpers, name="helpers")
