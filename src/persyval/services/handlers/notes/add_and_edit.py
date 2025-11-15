import datetime
from typing import TYPE_CHECKING

import typer

from persyval.models.note import Note
from persyval.services.data_actions.note_add import note_add
from persyval.services.data_actions.note_update import note_update
from persyval.utils.format import render_canceled_message, render_good_message

if TYPE_CHECKING:
    import rich

    from persyval.services.data_storage.data_storage import DataStorage


def note_add_for_handler(
    console: rich.console.Console,
    data_storage: DataStorage,
) -> Note | None:
    content = open_editor_template(note=None)

    if not content:
        render_good_message(
            console,
            f"{Note.get_meta_info().singular_name} creation cancelled "
            f"or empty {Note.get_meta_info().singular_name.lower()} discarded.",
        )
        return None

    title, body = extract_title_and_body(content)
    note = Note(title=title, content=body)

    note = note_add(data_storage=data_storage, note=note)
    render_good_message(console, f"{Note.get_meta_info().singular_name} '{title}' added successfully.")

    return note


def note_edit_for_handler(
    console: rich.console.Console,
    data_storage: DataStorage,
    note: Note,
) -> None:
    content = open_editor_template(note)

    if content is None:
        render_canceled_message(console, "Edit operation cancelled or no changes made.")
        return

    new_title, new_body = extract_title_and_body(content)

    note_update(data_storage, note.uid, new_title, new_body)

    render_good_message(
        console,
        f"{Note.get_meta_info().singular_name} '{new_title}' updated successfully.",
    )

    return


def open_editor_template(note: Note | None) -> str | None:
    """Open the system editor and return written text, or None if canceled."""
    template = form_editor_template(note)

    edited = typer.edit(template)

    return None if edited is None else edited.strip() or None


def clean(section: str) -> str:
    return "\n".join(line for line in section.splitlines() if line.strip() and not line.strip().startswith("#")).strip()


def extract_title_and_body(content: str) -> tuple[str, str]:
    """Split editor content into title and body sections."""
    marker = "# Enter body of your note below."
    parts = content.split(marker, maxsplit=1)

    title_part = parts[0]
    body_part = parts[1] if len(parts) > 1 else ""

    # Clean both parts from comments and empty lines

    title = clean(title_part)
    body = clean(body_part)

    if not title:
        title = f"Note {datetime.datetime.now(datetime.UTC):%Y-%m-%d %H:%M}"
    if not body:
        body = "(No content)"

    return title, body


def form_editor_template(note: Note | None) -> str:
    template_title_data = note.title or "" if note else ""
    template_content_data = note.content or "" if note else ""

    return (
        "# Enter title of your note below.\n"
        "# Lines starting with '#' will be ignored.\n"
        f"{template_title_data}\n\n"
        "# Enter body of your note below.\n"
        "# Everything after this line will be the note body.\n\n"
        f"{template_content_data}\n"
    )
