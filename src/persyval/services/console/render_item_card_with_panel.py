from typing import TYPE_CHECKING, Final

from pydantic import BaseModel
from rich.markup import escape

from persyval.services.console.types import RichFormattedText
from persyval.utils.format import render_with_panel

if TYPE_CHECKING:
    from rich.console import Console


class RenderItem(BaseModel):
    name: str
    value: str | None

    no_escape_value: bool = False


RENDER_I_PLACEHOLDER: Final[str] = "-"
RENDER_I_STYLE: Final[str] = "green bold"


def render_item_card_with_panel(
    console: Console,
    entity_title: str,
    list_to_render: list[RenderItem],
) -> None:
    message_as_list: list[str] = []
    for item in list_to_render:
        value = item.value if item.value is not None else RENDER_I_PLACEHOLDER
        if not item.no_escape_value:
            value = escape(value)

        part = f"[{RENDER_I_STYLE}]{escape(item.name)}:[/{RENDER_I_STYLE}] {value}"
        message_as_list.append(part)

    message = "\n".join(message_as_list)

    render_with_panel(
        console=console,
        title=f"{entity_title} details",
        message=RichFormattedText(message),
        style=RENDER_I_STYLE,
    )
