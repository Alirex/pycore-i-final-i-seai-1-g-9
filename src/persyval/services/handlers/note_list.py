from typing import TYPE_CHECKING, Final

from rich.table import Table

from persyval.services.data_actions.note_list import note_list
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_canceled_message

if TYPE_CHECKING:
    from persyval.services.handlers_base.handler_output import HandlerOutput

MAX_CONTENT_WIDTH: Final[int] = 40
LONG_PLACEHOLDER: Final[str] = "..."


def _truncate_text(text: str, max_width: int) -> str:
    cleaned_text = text.replace(chr(10), " ")

    if len(cleaned_text) > max_width:
        size = max_width - len(LONG_PLACEHOLDER)
        return f"{cleaned_text[:size]}{LONG_PLACEHOLDER}"
    return cleaned_text


class NoteListIHandler(
    HandlerBase,
):
    def _handler(self) -> HandlerOutput | None:
        notes = note_list(data_storage=self.data_storage)
        if not notes:
            render_canceled_message(self.console, "No notes found in storage.")
            return None

        table = Table(
            show_header=True,
            header_style="bold cyan",
        )

        table.add_column("UID", style="dim")
        table.add_column("Title", style="bold")
        table.add_column("Content")

        for note in notes:
            title_str = note.title if note.title is not None else "[No Title]"

            content_str = _truncate_text(note.content, MAX_CONTENT_WIDTH)

            table.add_row(
                str(note.uid),
                title_str,
                content_str,
            )

        self.console.print(table)

        return None
