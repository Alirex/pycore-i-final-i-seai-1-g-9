from typing import Final

BOOL_TRUE_VALUES: Final[set[str]] = {"1", "true", "yes", "y", "on"}
BOOL_FALSE_VALUES: Final[set[str]] = {"0", "false", "no", "n", "off"}


def convert_command_part_to_bool(part: str | bool) -> bool:  # noqa: FBT001
    if isinstance(part, bool):
        return part

    part = part.strip().lower()

    if part in BOOL_TRUE_VALUES:
        return True

    if part in BOOL_FALSE_VALUES:
        return False

    msg = f"Invalid boolean value: {part}"
    raise ValueError(msg)
