from typing import Protocol, Self

from pydantic import BaseModel, Field

from persyval.services.model_meta.field_meta import FieldsMetaConfig


class ModelMetaInfo(BaseModel):
    singular_name: str = Field(description="Singular name of the model. Write with a capital letter.")
    plural_name: str = Field(description="Plural name of the model. Write with a capital letter.")

    fields_meta_config: FieldsMetaConfig = Field(
        default_factory=FieldsMetaConfig,
        description="Metadata configuration for the model's fields.",
    )

    @classmethod
    def from_class(
        cls,
        _cls: type[BaseModel],
        fields_meta_config: FieldsMetaConfig | None = None,
    ) -> Self:
        return cls(
            singular_name=_cls.__name__,
            plural_name=f"{_cls.__name__}s",
            #
            fields_meta_config=fields_meta_config or FieldsMetaConfig(),
        )


class HaveMetaInfoProtocol(Protocol):
    @classmethod
    def get_meta_info(cls) -> ModelMetaInfo: ...
