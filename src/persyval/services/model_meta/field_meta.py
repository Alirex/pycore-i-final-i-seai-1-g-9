import enum
from collections.abc import Callable
from typing import Annotated, Any

from pydantic import BaseModel, Field


@enum.unique
class FilterMode(enum.StrEnum):
    EXACT = "exact"
    PARTIAL = "partial"


class FieldItemMetaConfig(BaseModel):
    name: Annotated[str, Field(description="The name of the field.")]
    aliases: list[str] = Field(default_factory=list, description="List of aliases for the field.")

    description: Annotated[str | None, Field(description="The description of the field.")] = None

    parse_func: Annotated[Callable[[Any], Any] | None, Field(description="Function to parse the field value.")] = None

    is_list_based: bool = Field(
        default=False,
        description="Indicates if the field is list-based.",
    )

    is_filterable: bool = Field(
        default=True,
        description="Indicates if the field can be used for filtering.",
    )
    filter_mode: FilterMode = Field(
        default=FilterMode.PARTIAL,
        description="The filtering mode for the field.",
    )

    is_sortable: bool = Field(
        default=True,
        description="Indicates if the field can be used for sorting.",
    )

    is_groupable: bool = Field(
        default=True,
        description="Indicates if the field can be used for grouping.",
    )
    # is_editable: bool = Field(
    #     default=True,
    #     description="Indicates if the field is editable.",
    # )


class FieldsMetaConfig(BaseModel):
    fields: list[FieldItemMetaConfig] = Field(
        default_factory=list,
        description="List of field metadata configurations.",
    )

    def get_fields_meta_registry(self) -> dict[str, FieldItemMetaConfig]:
        return {field.name: field for field in self.fields}

    def get_field_name_fact(self, field_name: str) -> str:
        field_name = field_name.strip().lower()
        for field in self.fields:
            if field.name == field_name or field_name in field.aliases:
                return field.name

        msg = f"Field with name or alias '{field_name}' not found."
        raise KeyError(msg)

    def get_fields_for_filtering(self) -> list[FieldItemMetaConfig]:
        return [field for field in self.fields if field.is_filterable]

    def get_field_names_for_filtering(self) -> list[str]:
        return [field.name for field in self.get_fields_for_filtering()]

    def get_fields_for_sorting(self) -> list[FieldItemMetaConfig]:
        return [field for field in self.fields if field.is_sortable]

    def get_field_names_for_sorting(self) -> list[str]:
        return [field.name for field in self.get_fields_for_sorting()]
