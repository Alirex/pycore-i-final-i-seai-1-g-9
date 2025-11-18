from typing import TYPE_CHECKING, override

from prompt_toolkit.completion import CompleteEvent, Completer, Completion
from pydantic import BaseModel

from persyval.services.commands.iterate_over_commands_meta import iterate_over_commands_meta

if TYPE_CHECKING:
    from collections.abc import Iterable

    from prompt_toolkit.document import Document


class HintsCompleter(Completer, BaseModel):
    hints: list[str]

    @override
    def get_completions(
        self,
        document: Document,
        complete_event: CompleteEvent,
    ) -> Iterable[Completion]:
        del complete_event

        text = document.text_before_cursor

        if " " in text.lstrip():
            return

        word = document.get_word_before_cursor().lower()

        for hint in self.hints:
            if hint.startswith(word):
                yield Completion(hint, start_position=-len(word))


def get_completer(*, use_advanced_completer: bool = False) -> HintsCompleter:
    return HintsCompleter(
        hints=[
            str(command_meta.command) for command_meta in iterate_over_commands_meta(show_hidden=use_advanced_completer)
        ],
    )
