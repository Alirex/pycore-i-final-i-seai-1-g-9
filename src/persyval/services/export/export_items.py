import csv
from typing import TYPE_CHECKING, Any

from persyval.utils.format import render_canceled_message, render_error

if TYPE_CHECKING:
    import pathlib
    from collections.abc import Iterable

    from pydantic import BaseModel
    from rich.console import Console


def adapt_fields_to_csv(
    item: dict[str, Any],
) -> dict[str, Any]:
    for key, value in item.items():
        if isinstance(value, list):
            item[key] = ",".join(value)
    return item


def write_to_csv(
    console: Console,
    items: Iterable[BaseModel],
    export_path: pathlib.Path,
) -> bool:
    if not items:
        render_canceled_message(
            console=console,
            message="No items to export.",
        )

        return False

    try:
        with export_path.open("w", newline="", encoding="utf-8") as f:
            iter_items = iter(items)

            first = next(iter_items)
            fields = first.model_fields.keys()

            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()

            writer.writerow(adapt_fields_to_csv(first.model_dump(mode="json")))

            for contact in items:
                writer.writerow(adapt_fields_to_csv(contact.model_dump(mode="json")))

    except OSError as e:
        render_error(
            console,
            message=f"Failed to export contacts: {e}",
            title="File Error",
        )
        return False

    else:
        return True
