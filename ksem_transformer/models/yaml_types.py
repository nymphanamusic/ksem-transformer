from typing import Literal, NotRequired, TypedDict

type KeyswitchField = Literal[
    "name",
    "key",
    "second_key",
    "bank",
    "sub",
    "program",
    "cc_n",
    "cc_v",
    "chain",
    "color",
]

MetaSettings = TypedDict(
    "MetaSettings",
    {
        "comment_template": str,
        "colors": dict[str, list[int]],
        "middle_c": Literal["C3", "C4", "C5"],
    },
    total=False,
)

InstrumentKeyswitches = TypedDict(
    "InstrumentKeyswitches",
    {
        "root_octaves": dict[Literal["key", "second_key"], int],
        "mapping": list[KeyswitchField],
        "values": list[list[str | int]],
    },
)

Instrument = TypedDict("Instrument", {"keyswitches": InstrumentKeyswitches})
InstrumentGroup = TypedDict(
    "InstrumentGroup",
    {"meta_settings": NotRequired[MetaSettings], "instruments": dict[str, Instrument]},
)
Product = TypedDict(
    "Product",
    {
        "meta_settings": NotRequired[MetaSettings],
        "instrument_groups": dict[str, InstrumentGroup],
    },
)
MappingFile = TypedDict(
    "MappingFile",
    {
        "meta_settings": NotRequired[MetaSettings],
        "products": dict[str, Product],
    },
)
