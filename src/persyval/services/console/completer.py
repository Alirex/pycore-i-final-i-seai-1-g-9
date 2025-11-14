from typing import TYPE_CHECKING

from prompt_toolkit.completion import CompleteEvent, Completer, Completion
from pydantic import BaseModel

from persyval.services.commands.iterate_over_commands_meta import iterate_over_commands_meta

if TYPE_CHECKING:
    from collections.abc import Iterable

    from prompt_toolkit.document import Document


class HintsCompleter(Completer, BaseModel):
    hints: list[str]

    def get_completions(
        self,
        document: Document,
        complete_event: CompleteEvent,  # noqa: ARG002
    ) -> Iterable[Completion]:
        text = document.text_before_cursor

        if " " in text.lstrip():
            return

        word = document.get_word_before_cursor().lower()

        for hint in self.hints:
            if hint.startswith(word):
                yield Completion(hint, start_position=-len(word))


def get_completer() -> HintsCompleter:
    return HintsCompleter(hints=[str(command_meta.command) for command_meta in iterate_over_commands_meta()])
