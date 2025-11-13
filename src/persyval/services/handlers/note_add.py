from datetime import UTC, datetime
from typing import TYPE_CHECKING

import click
from pydantic import BaseModel

from persyval.models.note import Note
from persyval.services.commands.command_meta import ArgMetaConfig, ArgsConfig
from persyval.services.data_actions.note_add import note_add
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_good_message

if TYPE_CHECKING:
    from persyval.services.handlers_base.handler_output import HandlerOutput


class NoteAddIArgs(BaseModel):
    content: str
    title: str | None = None


NOTE_ADD_I_ARGS_CONFIG = ArgsConfig[NoteAddIArgs](
    result_cls=NoteAddIArgs,
    args=[
        ArgMetaConfig(name="content", required=False),
        ArgMetaConfig(name="title", required=False),
    ],
)


class NoteAddIHandler(HandlerBase):
    def _handler(self) -> HandlerOutput | None:
        content = self._open_editor_template()

        if not content:
            render_good_message(self.console, "Note creation cancelled or empty note discarded.")
            return None

        title, body = self._extract_title_and_body(content)

        note = Note(title=title, content=body)
        note_add(data_storage=self.data_storage, note=note)

        render_good_message(self.console, f"Note '{title}' added successfully.")
        return None

    def _open_editor_template(self) -> str | None:
        """Open system editor via click.edit() and return written text, or None if cancelled."""
        template = (
            "# Enter title of your note below.\n"
            "# Lines starting with '#' will be ignored.\n"
            "\n"
            "\n"
            "# Enter body of your note below.\n"
            "# Everything after this line will be the note body.\n\n"
        )

        edited = click.edit(template)
        if edited is None:
            return None

        return edited.strip() or None

    def _extract_title_and_body(self, content: str) -> tuple[str, str]:
        """Split editor content into title and body sections."""
        marker = "# Enter body of your note below."
        parts = content.split(marker, maxsplit=1)

        title_part = parts[0]
        body_part = parts[1] if len(parts) > 1 else ""

        # Clean both parts from comments and empty lines
        def clean(section: str) -> str:
            return "\n".join(
                line for line in section.splitlines() if line.strip() and not line.strip().startswith("#")
            ).strip()

        title = clean(title_part)
        body = clean(body_part)

        if not title:
            title = f"Note {datetime.now(UTC):%Y-%m-%d %H:%M}"
        if not body:
            body = "(No content)"

        return title, body
