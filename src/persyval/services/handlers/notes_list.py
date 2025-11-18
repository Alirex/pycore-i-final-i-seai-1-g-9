from collections import defaultdict
from typing import TYPE_CHECKING, cast

from prompt_toolkit import HTML, choice, print_formatted_text

from persyval.constants.text import CHOICE_I_TO_MAIN_MENU
from persyval.models.note import (
    Note,
    NoteUid,
)
from persyval.services.console.add_option_i_to_main_menu import (
    add_option_i_to_main_menu,
)
from persyval.services.data_actions.notes_list import (
    NotesListConfig,
    note_list,
)
from persyval.services.handlers.notes.note_item_ask_next_action import (
    note_item_ask_next_action,
)
from persyval.services.handlers.shared.sort_and_filter import (
    LIST_I_ARGS_CONFIG_NOTES,
    ListIArgs,
)
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_canceled_message

if TYPE_CHECKING:
    from persyval.services.commands.args_config import ArgsConfig
    from persyval.services.console.types import PromptToolkitFormattedText


# TODO: Make repeatable filtering without exiting to main menu


def notes_by_tag(notes: list[Note]) -> dict[str, list[Note]]:
    tag_dict: dict[str, list[Note]] = defaultdict(list)

    for note in notes:
        if note.tags:  # note has tags
            for tag in note.tags:
                normalized_tag = tag.strip().lower()
                tag_dict[normalized_tag].append(note)
        else:  # optionally handle notes without tags under a special key
            tag_dict["(No tag)"].append(note)

    return dict(tag_dict)


def choose_from_list(
    message: str,
    items: list[tuple[NoteUid | str | None, PromptToolkitFormattedText]],
) -> NoteUid | str | None:
    """Show a choice list to the user and return the selected UID (or None).

    Adds a special 'i' option for returning to the main menu.
    """
    options_list: list[tuple[NoteUid | str | None, PromptToolkitFormattedText]] = []
    add_option_i_to_main_menu(options_list)
    options_list.extend(items)

    return choice(
        message=message,
        options=options_list,
    )


class NotesListIHandler(
    HandlerBase[ListIArgs],
):
    def _get_args_config(self) -> ArgsConfig[ListIArgs]:
        return LIST_I_ARGS_CONFIG_NOTES

    def _make_action(self, parsed_args: ListIArgs) -> None:
        list_config = NotesListConfig(
            **parsed_args.model_dump(),
        )

        notes = note_list(
            data_storage=self.data_storage,
            list_config=list_config,
        )

        if self.plain_render:
            for note in notes:
                print(note.uid)
            return

        if self.non_interactive:
            for note in notes:
                print_formatted_text(note.get_prompt_toolkit_output())
            return

        if not notes:
            render_canceled_message(
                self.console,
                f"No {Note.get_meta_info().plural_name.lower()} found.",
                title="Not found",
            )
            return

        tags_dict = notes_by_tag(notes)
        sorted_tags_list = sorted(
            tags_dict.keys(),
            key=lambda tag: (tag == "(No tag)", tag),
        )

        tag_options: list[tuple[NoteUid | str | None, HTML | str]] = [
            (tag, HTML(f"<b>{tag}</b>")) for tag in sorted_tags_list
        ]
        message_after_filter = (
            f"{Note.get_meta_info().plural_name} found: {len(notes)}. \nChoose tag group to interact:"
        )

        choice_by_list = choose_from_list(message_after_filter, tag_options)

        if choice_by_list is None:
            return

        if choice_by_list is not CHOICE_I_TO_MAIN_MENU:
            tag_notes = tags_dict[str(choice_by_list)]
            tag_options = [(note.uid, note.get_prompt_toolkit_output()) for note in tag_notes]
            message_after_tag_filter = (
                f"{Note.get_meta_info().plural_name} found: {len(tag_notes)}. \nChoose note to interact:"
            )

            choice_by_tag_list = choose_from_list(message_after_tag_filter, tag_options)

            if choice_by_tag_list is None:
                return

            note_item_ask_next_action(
                execution_queue=self.execution_queue,
                uid=cast("NoteUid", choice_by_tag_list),
            )

        return
