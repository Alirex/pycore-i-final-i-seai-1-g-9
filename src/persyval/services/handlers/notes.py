import enum
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Final

import typer
from prompt_toolkit import choice, shortcuts
from rich import box, table, text

from persyval.models.note import Note, NoteUid
from persyval.services.commands.command_meta import ArgMetaConfig, ArgsConfig
from persyval.services.data_actions.note_add import note_add
from persyval.services.data_actions.note_delete import note_delete
from persyval.services.data_actions.note_list import note_list
from persyval.services.data_actions.note_update import note_update
from persyval.services.execution_queue.execution_queue import HandlerArgsBase
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_canceled_message, render_good_message

if TYPE_CHECKING:
    from persyval.services.handlers_base.handler_output import HandlerOutput

MAX_CONTENT_WIDTH: Final[int] = 100
LONG_PLACEHOLDER: Final[str] = "..."


class NoteItemsActions(enum.StrEnum):
    ADD = "add"
    EDIT = "edit"
    DELETE = "delete"
    VIEW = "view"


class NotesListIArgs(HandlerArgsBase):
    actions: NoteItemsActions | None = None


NOTES_I_ARGS_CONFIG = ArgsConfig[NotesListIArgs](
    result_cls=NotesListIArgs,
    args=[
        ArgMetaConfig(
            name="actions",
            parser_func=lambda x: NoteItemsActions(x) if x else None,
        ),
    ],
)


class NotesIHandler(
    HandlerBase[NotesListIArgs],
):
    def _get_args_config(self) -> ArgsConfig[NotesListIArgs]:
        return NOTES_I_ARGS_CONFIG

    def _make_action(self, parsed_args: NotesListIArgs) -> HandlerOutput | None:
        if parsed_args.actions is not None:
            choice_result = parsed_args.actions
        else:
            choice_result = choice(
                message="Choose action:",
                options=[(item, item.value.capitalize()) for item in NoteItemsActions],
            )

        match choice_result:
            case NoteItemsActions.ADD:
                self._handler_add()

            case NoteItemsActions.VIEW:
                self._handler_view()

            case NoteItemsActions.EDIT:
                self._handler_edit()

            case NoteItemsActions.DELETE:
                self._handler_delete()

            case _:
                return None

        return None

    def _handler_add(self) -> HandlerOutput | None:
        content = self._open_editor_template(None)

        if not content:
            render_good_message(self.console, "Note creation cancelled or empty note discarded.")
            return None

        title, body = self._extract_title_and_body(content)
        note = Note(title=title, content=body)

        note_add(data_storage=self.data_storage, note=note)
        render_good_message(self.console, f"Note '{title}' added successfully.")

        return None

    def _handler_view(self) -> HandlerOutput | None:
        notes = note_list(data_storage=self.data_storage)
        if not notes:
            render_canceled_message(self.console, "No notes found in storage.")
            return None

        notes_table = table.Table(
            title="📒 Notes List",
            title_style="bold frame",
            show_header=True,
            header_style="bold cyan",
            leading=True,
            box=box.SIMPLE_HEAVY,
        )

        notes_table.add_column("No.", style="light_cyan3", max_width=10, justify="center")
        notes_table.add_column("Title", style="light_cyan3", max_width=50, no_wrap=True)
        notes_table.add_column("Content", style="light_cyan3", max_width=MAX_CONTENT_WIDTH, overflow="fold")

        for index, note in enumerate(notes):
            title_str = text.Text(note.title or "[No Title]", style="bold")
            content_str = text.Text(self._truncate_text(note.content, MAX_CONTENT_WIDTH), style="dim")
            notes_table.add_row(
                str(index + 1),
                title_str,
                content_str,
            )

        self.console.print(notes_table)
        return None

    def _handler_edit(self) -> HandlerOutput | None:
        notes = note_list(data_storage=self.data_storage)
        if not notes:
            render_canceled_message(self.console, "No notes found in storage.")
            return None

        selected_note_id = self._get_note_id()
        filtered_notes = list(filter(lambda n: n.uid == selected_note_id, notes))
        if not filtered_notes:
            render_canceled_message(self.console, "No note with indicated id found in storage.")
            return None

        target_note = filtered_notes[0]
        edited = self._open_editor_template(target_note)

        if edited is None:
            render_canceled_message(self.console, "Edit operation cancelled or no changes made.")
            return None

        new_title, new_body = self._extract_title_and_body(edited)
        note_update(self.data_storage, selected_note_id, new_title, new_body)

        render_good_message(
            self.console,
            f"Note '{new_title}' updated successfully.",
        )

        return None

    def _handler_delete(self) -> HandlerOutput | None:
        notes = note_list(data_storage=self.data_storage)
        if not notes:
            render_canceled_message(self.console, "No notes found in storage.")
            return None

        selected_note_id = self._get_note_id()

        is_do = shortcuts.yes_no_dialog(
            title="Confirm Note Delete",
            text="Are you sure you want to delete the note?",
        ).run()

        if not is_do:
            render_canceled_message(
                self.console,
                "Note delete operation cancelled by user.",
            )
            return None

        note_delete(data_storage=self.data_storage, note_uid=selected_note_id)

        render_good_message(
            self.console,
            f"Note with uid {selected_note_id} has been removed.",
        )

        return None

    def _open_editor_template(self, note: Note | None) -> str | None:
        """Open system editor via click.edit() and return written text, or None if cancelled."""
        template = self._form_editor_template(note)

        edited = typer.edit(template)
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

    def _truncate_text(self, text: str, max_width: int) -> str:
        cleaned_text = text.replace(chr(10), " ")

        if len(cleaned_text) > max_width:
            size = max_width - len(LONG_PLACEHOLDER)
            return f"{cleaned_text[:size]}{LONG_PLACEHOLDER}"
        return cleaned_text

    def _get_note_id(self) -> NoteUid:
        notes = note_list(data_storage=self.data_storage)

        selected_note_id: NoteUid = choice(
            message="Choose a note:",
            options=[(note.uid, note.title) for note in notes],
        )

        return selected_note_id

    def _form_editor_template(self, note: Note | None) -> str:
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
