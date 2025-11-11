from goit_i_pycore_i_personal_assistant.services.commands.commands_enum import COMMANDS_ORDER, Command
from goit_i_pycore_i_personal_assistant.services.commands.commands_meta_registry import COMMANDS_META_REGISTRY


def test_command_registry_add_command() -> None:
    used_keys = set(COMMANDS_META_REGISTRY.keys())
    all_keys = set(Command)

    difference = all_keys - used_keys
    assert len(difference) == 0, [str(item) for item in difference]


def test_commands_order() -> None:
    used_keys = set(COMMANDS_ORDER)
    all_keys = set(Command)

    difference = all_keys - used_keys
    assert len(difference) == 0, [str(item) for item in difference]
