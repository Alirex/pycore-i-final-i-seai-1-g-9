from goit_i_pycore_i_personal_assistant.cli.chat.main import app as app_chat
from goit_i_pycore_i_personal_assistant.cli.main import app as app_full


def main() -> None:
    app_full()


def main_short() -> None:
    app_chat()
