import enum

from pydantic import BaseModel, Field

from persyval.services.commands.args_config import ArgMetaConfig, ArgsConfig, ArgType
from persyval.services.execution_queue.execution_queue import HandlerArgsBase


@enum.unique
class ListOrderModeEnum(enum.StrEnum):
    DEFAULT = enum.auto()
    CUSTOM = enum.auto()


@enum.unique
class ListFilterModeEnum(enum.StrEnum):
    ALL = enum.auto()
    FILTER = enum.auto()


class ListModeMeta[T](BaseModel):
    mode: T
    title: str


ListFilterModeMeta = ListModeMeta[ListFilterModeEnum]
ListOrderModeMeta = ListModeMeta[ListOrderModeEnum]


class ListIArgs(HandlerArgsBase):
    # order_mode: ListOrderModeEnum | None = None
    filter_mode: ListFilterModeEnum | None = None
    queries: list[str] | None = None


LIST_I_ARGS_CONFIG = ArgsConfig[ListIArgs](
    result_cls=ListIArgs,
    args=[
        # ArgMetaConfig(
        #     name="order_mode",
        #     parser_func=lambda x: ListOrderModeEnum(x) if x else None,
        # ),
        ArgMetaConfig(
            name="filter_mode",
            parser_func=lambda x: ListFilterModeEnum(x) if x else None,
        ),
        ArgMetaConfig(
            name="queries",
            type_=ArgType.LIST_BY_COMMA,
            default_factory=list,
        ),
    ],
)

LIST_FILTER_MODE_REGISTRY: dict[ListFilterModeEnum, ListFilterModeMeta] = {
    item.mode: item
    for item in [
        ListFilterModeMeta(
            mode=ListFilterModeEnum.ALL,
            title="Show all",
        ),
        ListFilterModeMeta(
            mode=ListFilterModeEnum.FILTER,
            title="Filter",
        ),
    ]
}


LIST_ORDER_MODE_REGISTRY: dict[ListOrderModeEnum, ListOrderModeMeta] = {
    item.mode: item
    for item in [
        ListOrderModeMeta(
            mode=ListOrderModeEnum.DEFAULT,
            title="Use default",
        ),
        ListOrderModeMeta(
            mode=ListOrderModeEnum.CUSTOM,
            title="Customize",
        ),
    ]
}


class ListConfig[T](BaseModel):
    filter_mode: ListFilterModeEnum

    queries_as_map: dict[T, str] = Field(default_factory=dict)
