from typing import Self

from pydantic import BaseModel, Field


class ModelMetaInfo(BaseModel):
    singular_name: str = Field(description="Singular name of the model. Write with a capital letter.")
    plural_name: str = Field(description="Plural name of the model. Write with a capital letter.")

    @classmethod
    def from_class(
        cls,
        _cls: type[BaseModel],
    ) -> Self:
        return cls(
            singular_name=_cls.__name__,
            plural_name=f"{_cls.__name__}s",
        )
