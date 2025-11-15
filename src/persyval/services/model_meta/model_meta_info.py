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
            singular_name=cls.__name__.lower(),
            plural_name=f"{cls.__name__.lower()}s",
        )
