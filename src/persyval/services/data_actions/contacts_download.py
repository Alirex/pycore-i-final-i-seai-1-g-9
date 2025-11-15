import csv
from typing import TYPE_CHECKING

from persyval.utils.format import render_error

if TYPE_CHECKING:
    import pathlib
    from collections.abc import Iterable

    from rich.console import Console

    from persyval.models.contact import Contact


def write_contacts_to_csv(
    console: Console,
    contacts: Iterable[Contact],
    export_path: pathlib.Path,
) -> bool:
    try:
        with export_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            writer.writerow(
                ["uid", "name", "phones", "emails", "address", "birthday"],
            )

            for contact in contacts:
                writer.writerow(
                    [
                        str(contact.uid),
                        contact.name,
                        ",".join(contact.phones),
                        ",".join(contact.emails),
                        contact.address or "",
                        contact.birthday.isoformat() if contact.birthday else "",
                    ],
                )
                writer.writerow([])

    except OSError as e:
        render_error(
            console,
            message=f"Failed to export contacts: {e}",
            title="File Error",
        )
        return False

    else:
        return True
