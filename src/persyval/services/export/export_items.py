import csv
import json
from typing import TYPE_CHECKING, Any

from persyval.exceptions.main import NotFoundError

if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path

    from pydantic import BaseModel


def adapt_fields_to_csv(
    item: dict[str, Any],
) -> dict[str, Any]:
    for key, value in item.items():
        if isinstance(value, list):
            item[key] = ",".join(str(v) for v in value)
    return item


def write_to_csv(
    items: Iterable[BaseModel],
    path: Path,
) -> None:
    iter_items = iter(items)

    try:
        first = next(iter_items)
    except StopIteration:
        msg = "No items to export."
        raise NotFoundError(msg) from None

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        fields = type(first).model_fields.keys()

        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerow(adapt_fields_to_csv(first.model_dump(mode="json")))

        for item in iter_items:
            writer.writerow(adapt_fields_to_csv(item.model_dump(mode="json")))


def write_to_json(
    *,
    items: Iterable[BaseModel],
    path: Path,
) -> None:
    data = [item.model_dump(mode="json") for item in items]

    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
