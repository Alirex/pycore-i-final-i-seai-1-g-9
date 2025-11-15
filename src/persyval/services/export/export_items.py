import csv
from typing import TYPE_CHECKING, Any

from persyval.exceptions.main import NotFoundError

if TYPE_CHECKING:
    import pathlib
    from collections.abc import Iterable

    from pydantic import BaseModel


def adapt_fields_to_csv(
    item: dict[str, Any],
) -> dict[str, Any]:
    for key, value in item.items():
        if isinstance(value, list):
            item[key] = ",".join(value)
    return item


def write_to_csv(
    items: Iterable[BaseModel],
    path: pathlib.Path,
) -> None:
    if not items:
        msg = "No items to export."
        raise NotFoundError(msg)

    path.parent.mkdir(parents=True, exist_ok=True)

    # sourcery skip: extract-method
    with path.open("w", newline="", encoding="utf-8") as f:
        iter_items = iter(items)

        first = next(iter_items)
        fields = first.model_fields.keys()

        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()

        writer.writerow(adapt_fields_to_csv(first.model_dump(mode="json")))

        for contact in items:
            writer.writerow(adapt_fields_to_csv(contact.model_dump(mode="json")))
