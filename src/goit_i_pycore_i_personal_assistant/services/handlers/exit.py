from goit_i_pycore_i_personal_assistant.exceptions.invalid_command_error import InvalidCommandError
from goit_i_pycore_i_personal_assistant.services.handlers_base.handler_base import HandlerBase
from goit_i_pycore_i_personal_assistant.services.handlers_base.handler_output import HandlerOutput
from goit_i_pycore_i_personal_assistant.utils.format import format_good_message


# noinspection PyTypeChecker
class ExitIHandler(HandlerBase[None, None]):
    def _parse_args(self) -> None:
        if self.args:
            msg = "Command does not take any arguments."
            raise InvalidCommandError(msg)

    def _make_action(self, parsed_args: None) -> None:
        pass

    def _get_or_render_output(
        self,
        output_data: None,  # noqa: ARG002
    ) -> HandlerOutput:
        return HandlerOutput(message_rich=format_good_message("Goodbye!"), is_exit=True)
