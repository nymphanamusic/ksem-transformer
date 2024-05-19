from collections.abc import Callable
from typing import Any, Literal, Pattern, Unpack

from pydantic import AliasChoices, AliasPath, Discriminator, Field
from pydantic.config import JsonDict
from pydantic.fields import (
    Deprecated,
    _EmptyKwargs,  # pyright: ignore[reportPrivateUsage]
    _Unset,  # pyright: ignore[reportPrivateUsage]
)
from pydantic_core import PydanticUndefined


def serial_field(
    serialization_alias: str,
    default: Any = PydanticUndefined,
    *,
    default_factory: Callable[[], Any] | None = _Unset,
    alias: str | None = _Unset,
    alias_priority: int | None = _Unset,
    validation_alias: str | AliasPath | AliasChoices | None = _Unset,
    title: str | None = _Unset,
    description: str | None = _Unset,
    examples: list[Any] | None = _Unset,
    exclude: bool | None = _Unset,
    discriminator: str | Discriminator | None = _Unset,
    deprecated: Deprecated | str | bool | None = _Unset,
    json_schema_extra: JsonDict | Callable[[JsonDict], None] | None = _Unset,
    frozen: bool | None = _Unset,
    validate_default: bool | None = _Unset,
    repr: bool = _Unset,
    init: bool | None = _Unset,
    init_var: bool | None = _Unset,
    kw_only: bool | None = _Unset,
    pattern: str | Pattern[str] | None = _Unset,
    strict: bool | None = _Unset,
    coerce_numbers_to_str: bool | None = _Unset,
    gt: float | None = _Unset,
    ge: float | None = _Unset,
    lt: float | None = _Unset,
    le: float | None = _Unset,
    multiple_of: float | None = _Unset,
    allow_inf_nan: bool | None = _Unset,
    max_digits: int | None = _Unset,
    decimal_places: int | None = _Unset,
    min_length: int | None = _Unset,
    max_length: int | None = _Unset,
    union_mode: Literal["smart", "left_to_right"] = _Unset,
    **extra: Unpack[_EmptyKwargs]
) -> Any:
    return Field(
        default=default,
        default_factory=default_factory,
        alias=alias,
        alias_priority=alias_priority,
        validation_alias=validation_alias,
        serialization_alias=serialization_alias,
        title=title,
        description=description,
        examples=examples,
        exclude=exclude,
        discriminator=discriminator,
        deprecated=deprecated,
        json_schema_extra=json_schema_extra,
        frozen=frozen,
        validate_default=validate_default,
        repr=repr,
        init=init,
        init_var=init_var,
        kw_only=kw_only,
        pattern=pattern,
        strict=strict,
        coerce_numbers_to_str=coerce_numbers_to_str,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        min_length=min_length,
        max_length=max_length,
        union_mode=union_mode,
        **extra,
    )
