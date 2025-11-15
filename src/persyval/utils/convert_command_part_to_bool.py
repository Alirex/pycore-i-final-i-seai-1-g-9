def convert_command_part_to_bool(part: str | bool) -> bool:  # noqa: FBT001
    if isinstance(part, bool):
        return part
    return part.lower() in {"1", "true", "yes", "y", "on"}
