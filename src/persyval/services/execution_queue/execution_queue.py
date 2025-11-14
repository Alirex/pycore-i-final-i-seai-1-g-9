import queue
from typing import NewType

from pydantic import BaseModel

from persyval.services.commands.commands_enum import Command


class HandlerArgsBase(BaseModel):
    """Base class for handler args.

    For type checking.
    """


class HandlerFullArgs(BaseModel):
    command: Command
    args: HandlerArgsBase | None = None


ExecutionQueue = NewType("ExecutionQueue", queue.Queue[HandlerFullArgs | str])


def create_execution_queue() -> ExecutionQueue:
    return ExecutionQueue(queue.Queue())
