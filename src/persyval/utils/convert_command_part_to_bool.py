def convert_command_part_to_bool(part: str) -> bool:
    return part.lower() in {"1", "true", "yes", "y", "on"}
