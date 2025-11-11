from persyval.cli.chat.main import app as app_chat
from persyval.cli.main import app as app_full


def main() -> None:
    app_full()


def main_short() -> None:
    app_chat()
