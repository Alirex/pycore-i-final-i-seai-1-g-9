from pydantic import BaseModel

from persyval.services.commands.command_meta import ArgMetaConfig, ArgsConfig, ArgType


class ArgsIForce(BaseModel):
    force: bool | None = None


ARGS_CONFIG_I_FORCE = ArgsConfig[ArgsIForce](
    result_cls=ArgsIForce,
    args=[
        ArgMetaConfig(
            name="force",
            type_=ArgType.BOOL,
        ),
    ],
)
