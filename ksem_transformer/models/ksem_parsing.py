from typing import Any, cast

from ksem_transformer.models.keyswitches import (
    Keyswitches,
    KeyswitchesRootOctaves,
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

    colors: list[tuple[int, ...]] = []
    notes = {"key": set[Note](), "second_key": set[Note]()}
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
                _note = Note.from_midi(raw_value, middle_c=settings.middle_c)
                notes[field].add(_note)
                # We throw out the octave and only use the note name for brevity
                row.append(_note.note)

            elif field == "color":
                # This is a color
                assert isinstance(raw_value, list)
                # We're keeping track of the unique colors and assigning identities
                # to them (from their list index)
                color = tuple(raw_value)
                if color not in colors:
                    colors.append(color)
                # The user will be responsible for assigning more useful color names
                row.append(f"Color{colors.index(color):02}")

            else:
                # This is some other unspecial value. We'll just use it raw
                assert isinstance(raw_value, (str, int))
                row.append(cast(Any, raw_value))

        if row:
            values.append(row)

    # Infer the root octaves of the keyswitch notes
    root_octaves = KeyswitchesRootOctaves()
    for _field_name in ("key", "second_key"):
        if _field_name not in mapping:
            continue
        # Make sure the notes span only one octave
        if min(notes[_field_name]).octave != max(notes[_field_name]).octave:
            raise ValueError(
                f"`{_field_name}` values span more than 1 octave. This is unexpected "
                "and ksem_transformer can't currently handle it."
            )
        setattr(root_octaves, _field_name, notes[_field_name].pop().octave)

    # Store the colors in the `Settings`
    for idx, color in enumerate(colors):
        color_int = color[0] | color[1] << 8 | color[2] << 16
        settings.colors[f"Color{idx:02}"] = f"#{color_int:6x}"

    return Keyswitches(root_octaves=root_octaves, mapping=mapping, values=values)
