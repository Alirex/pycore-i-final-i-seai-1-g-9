from persyval.services.commands.command_meta import ArgsConfig
from persyval.services.execution_queue.execution_queue import HandlerArgsBase


class ArgsIEmpty(HandlerArgsBase):
    pass


ARGS_CONFIG_I_EMPTY = ArgsConfig[ArgsIEmpty](
    result_cls=ArgsIEmpty,
    args=[],
)
