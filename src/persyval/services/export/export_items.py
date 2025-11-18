import csv
import json
from enum import Enum
from typing import TYPE_CHECKING, Any

from prompt_toolkit.shortcuts import choice

from persyval.exceptions.main import NotFoundError
from persyval.services.get_paths.get_app_dirs import get_downloads_dir_in_user_space
from persyval.utils.format import render_canceled_message, render_error, render_good_message

if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path

    from pydantic import BaseModel
    from rich.console import Console


class ExportFormat(str, Enum):
    CSV = "csv"
    JSON = "json"


format_choices = [
    (ExportFormat.CSV, "CSV"),
    (ExportFormat.JSON, "JSON"),
]


def choose_export_format(
    non_interactive: bool = False,  # noqa: FBT001, FBT002
) -> ExportFormat | None:
    if non_interactive:
        return ExportFormat.CSV
    return choice(
        message="Choose export format",
        options=format_choices,
    )


def ensure_overwrite_allowed(
    *,
    console: Console,
    export_path: Path,
    non_interactive: bool = False,
) -> bool:
    if not export_path.exists():
        return True

    console.print(f"[yellow]File already exists:\n{export_path.as_uri()}[/yellow]")

    if non_interactive:
        # TODO: Rework, to have better config for non-interactive mode.
        render_error(
            console,
            "Non-interactive mode: export forced.",
            title="Danger",
        )
        return True

    overwrite_choices = [
        (True, "Yes, overwrite the existing file"),
        (False, "No, cancel export"),
    ]

    return choice(
        message="Would you like to continue?",
        options=overwrite_choices,
    )


def adapt_fields_to_csv(
    item: dict[str, Any],
) -> dict[str, Any]:
    new_item: dict[str, Any] = {}

    for key, value in item.items():
        # Convert lists to a comma-separated string, converting nested structures to JSON where appropriate.
        if isinstance(value, list):
            parts: list[str] = []
            for elem in value:  # pyright: ignore[reportUnknownVariableType]
                if elem is None:
                    parts.append("")
                elif isinstance(elem, (dict, list)):
                    parts.append(json.dumps(elem, ensure_ascii=False))
                else:
                    parts.append(str(elem))  # pyright: ignore[reportUnknownArgumentType]
            new_item[key] = ",".join(parts)
        # Convert dicts to a JSON string so CSV cell contains a readable representation
        elif isinstance(value, dict):
            new_item[key] = json.dumps(value, ensure_ascii=False)

        else:
            new_item[key] = str(value)

    return new_item


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
    # TODO: Rework to better pydantic usage.
    data = [item.model_dump(mode="json") for item in items]

    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def export_items(
    *,
    console: Console,
    items: Iterable[BaseModel],
    file_base_name: str,
    chosen_format: ExportFormat,
    non_interactive: bool = False,
) -> None:
    extension = chosen_format.value
    export_path = get_downloads_dir_in_user_space() / f"{file_base_name}.{extension}"

    if not ensure_overwrite_allowed(
        console=console,
        export_path=export_path,
        non_interactive=non_interactive,
    ):
        render_canceled_message(console, "Export canceled by user.")
        return

    # export itself
    try:
        match chosen_format:
            case ExportFormat.CSV:
                write_to_csv(items=items, path=export_path)
            case ExportFormat.JSON:
                write_to_json(items=items, path=export_path)

    except Exception as exc:  # noqa: BLE001
        render_error(
            console,
            title=exc.__class__.__name__,
            message=f"Error while exporting to {export_path.as_uri()}: {exc}",
        )
        return

    render_good_message(
        console,
        f"Successfully exported to {export_path.as_uri()}",
    )
