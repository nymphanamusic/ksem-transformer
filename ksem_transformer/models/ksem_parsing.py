from typing import Any, cast

from ksem_transformer.models.keyswitches import (
    Keyswitches,
    KeyswitchField,
    keyswitch_field_to_ksem_key,
)
from ksem_transformer.models.ksem_json_types import EMPTY_VALUE, EmptyValue, KsemConfig
from ksem_transformer.models.settings.settings import Settings
from ksem_transformer.note import Note


def make_keyswitches(config: KsemConfig, settings: Settings) -> Keyswitches:
    mapping_order = list(keyswitch_field_to_ksem_key.keys())

    mapping = list[KeyswitchField](
        sorted(
            {
                cast(KeyswitchField, keyswitch_field_to_ksem_key.inv[field])
                for ks in config["ks"].values()
                for field, value in ks.items()
                if value != EMPTY_VALUE
            },
            key=lambda x: mapping_order.index(x),
        )
    )

    found_colors: list[tuple[int, ...]] = []

    values: list[list[Note | int | str]] = []
    for ks in config["ks"].values():
        row: list[Note | int | str] = []
        # Add each field from the mapping into this row
        for field in mapping:
            raw_value = cast(
                str | int | list[int] | EmptyValue,
                ks[keyswitch_field_to_ksem_key[field]],
            )

            if raw_value == EMPTY_VALUE:
                continue

            if field in ("key", "second_key"):
                # Notes should be converted from MIDI to Note
                assert isinstance(raw_value, int)
                row.append(Note.from_midi(raw_value))

            elif field == "color":
                # This is a color
                assert isinstance(raw_value, list)
                # We're keeping track of the unique colors and assigning identities
                # to them (from their list index)
                color = tuple(raw_value)
                if color not in found_colors:
                    found_colors.append(color)
                # The user will be responsible for assigning more useful color names
                row.append(f"Color{found_colors.index(color):02}")

            else:
                # This is some other unspecial value. We'll just use it raw
                assert isinstance(raw_value, (str, int))
                row.append(cast(Any, raw_value))

        if row:
            values.append(row)

    # Store the colors in the `Settings`
    for idx, color in enumerate(found_colors):
        color_int = color[0] | color[1] << 8 | color[2] << 16
        settings.colors[f"Color{idx:02}"] = f"#{color_int:6x}"

    return Keyswitches(mapping=mapping, values=values)
