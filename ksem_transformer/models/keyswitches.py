# Mapping of keyswitch fields to KSEM keys
from typing import Literal, cast

from bidict import bidict
from pydantic import BaseModel, ConfigDict, Field

from ksem_transformer.models.ksem_json_types import EMPTY_VALUE, KsemKeyswitchesEntry
from ksem_transformer.models.note_field import NoteField
from ksem_transformer.models.settings.settings import Settings
from ksem_transformer.note import Note, NoteLiteral
from ksem_transformer.utils.color import hex_color_to_tuple

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


keyswitch_field_to_ksem_key = bidict(
    {
        "name": "name",
        "key": "key",
        "second_key": "+key",
        "bank": "bnk",
        "sub": "sub",
        "program": "pgm",
        "cc_n": "ccn",
        "cc_v": "ccv",
        "chain": "chn",
        "color": "color",
    }
)


class KeyswitchesRootOctaves(BaseModel):
    """
    Represents the root octaves for keyswitches.
    """

    key: int | None = None
    second_key: int | None = None


class Keyswitches(BaseModel):
    """
    Represents the keyswitches configuration with root octaves, mapping, and values.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    root_octaves: KeyswitchesRootOctaves = Field(default_factory=KeyswitchesRootOctaves)
    mapping: list[KeyswitchField]
    values: list[list[NoteField | str | int]]

    def to_ksem_config(self, settings: Settings) -> dict[str, KsemKeyswitchesEntry]:
        """
        Converts the Keyswitches instance to a KsemKeyswitchesEntry configuration.
        """
        if "key" in self.mapping and self.root_octaves.key is None:
            raise ValueError(
                "`root_octaves.key` must be defined since you're mapping `key`"
            )
        if "second_key" in self.mapping and self.root_octaves.second_key is None:
            raise ValueError(
                "`root_octaves.second_key` must be defined since you're mapping "
                "`second_key`"
            )

        out: dict[str, KsemKeyswitchesEntry] = {}
        for row_idx, row in enumerate(self.values):
            row_out: KsemKeyswitchesEntry = {
                "name": EMPTY_VALUE,
                "key": EMPTY_VALUE,
                "+key": EMPTY_VALUE,
                "bnk": EMPTY_VALUE,
                "sub": EMPTY_VALUE,
                "pgm": EMPTY_VALUE,
                "ccn": EMPTY_VALUE,
                "ccv": EMPTY_VALUE,
                "chn": EMPTY_VALUE,
                "color": EMPTY_VALUE,
            }

            for value_idx, value in enumerate(row):
                ksem_key = keyswitch_field_to_ksem_key[self.mapping[value_idx]]

                if ksem_key == "key":
                    assert self.root_octaves.key is not None
                    assert isinstance(value, str)
                    row_out[ksem_key] = Note(
                        cast(NoteLiteral, value),
                        self.root_octaves.key,
                        middle_c=settings.middle_c,
                    ).to_midi()

                elif ksem_key == "+key":
                    assert self.root_octaves.second_key is not None
                    assert isinstance(value, str)
                    row_out[ksem_key] = Note(
                        cast(NoteLiteral, value),
                        self.root_octaves.second_key,
                        middle_c=settings.middle_c,
                    ).to_midi()

                elif ksem_key == "color":
                    assert isinstance(value, str)
                    row_out[ksem_key] = list(hex_color_to_tuple(settings.colors[value]))

                else:
                    row_out[ksem_key] = value

            out[str(row_idx + 1)] = row_out

        return out
