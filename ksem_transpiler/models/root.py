from __future__ import annotations

import json
from pathlib import Path
from typing import Literal, cast

import attrs
import yaml
from pydantic import BaseModel, ConfigDict, Field

from ksem_transpiler.models.ksem_json_types import (
    EMPTY_VALUE,
    KsemConfig,
    KsemCustomBank,
    KsemKeyswitchesEntry,
    KsemMidiControls,
)
from ksem_transpiler.note import Note, NoteLiteral

KSEM_VERSION = "4.2"


class MidiControl(BaseModel):
    """
    Represents a MIDI control with its enabled state, value, and optional MIDI CC number.
    """

    enabled: bool
    value: int
    midi_cc: int | None = None


# Mapping of internal MIDI control names to KSEM control names
midi_control_to_ksem = {
    "m01_modulation": "01Modulation",
    "m02_breath": "02Breath",
    "m04_foot": "04FootPedal",
    "m05_portamento": "05PortamentoTime",
    "m07_volume": "07Volume",
    "m10_pan": "10Pan",
    "m11_expression": "11Expression",
    "m64_hold": "64HoldPedal",
    "m65_portamento": "65PortamentoOnOff",
    "m66_sostenuto": "66SostenutoPedal",
    "m67_soft": "67SoftPedal",
    "m68_legato": "68LegatoPedal",
    "m71_resonance": "71Resonance",
    "m74_frequency": "74FrequencyCutoff",
    "m91_reverb": "91ReverbLevel",
    "m93_chorus": "93ChorusLevel",
    "custom_01": "CcCustom01",
    "custom_02": "CcCustom02",
    "custom_03": "CcCustom03",
    "custom_04": "CcCustom04",
    "custom_05": "CcCustom05",
    "custom_06": "CcCustom06",
    "custom_07": "CcCustom07",
    "custom_08": "CcCustom08",
}


class MidiControls(BaseModel):
    """
    Represents a collection of MIDI controls.
    """

    m01_modulation: MidiControl
    m02_breath: MidiControl
    m04_foot: MidiControl
    m05_portamento: MidiControl
    m07_volume: MidiControl
    m10_pan: MidiControl
    m11_expression: MidiControl
    m64_hold: MidiControl
    m65_portamento: MidiControl
    m66_sostenuto: MidiControl
    m67_soft: MidiControl
    m68_legato: MidiControl
    m71_resonance: MidiControl
    m74_frequency: MidiControl
    m91_reverb: MidiControl
    m93_chorus: MidiControl
    custom_01: MidiControl
    custom_02: MidiControl
    custom_03: MidiControl
    custom_04: MidiControl
    custom_05: MidiControl
    custom_06: MidiControl
    custom_07: MidiControl
    custom_08: MidiControl

    def to_ksem_config(self) -> KsemMidiControls:
        """
        Converts the MidiControls instance to a KsemMidiControls configuration.
        """
        out = cast(KsemMidiControls, {})
        for field_name in self.model_fields:
            ksem_key = midi_control_to_ksem[field_name]
            field = cast(MidiControl, getattr(self, field_name))

            out[f"{ksem_key}_button"] = int(field.enabled)
            out[f"{ksem_key}_dial"] = field.value
            if field.midi_cc is not None:
                out[f"{ksem_key}_num"] = field.midi_cc

        return out


# Mapping of internal MIDI control names to custom bank selection indices
midi_control_to_ksem_custom_bank_selection = {
    "m01_modulation": 1,
    "m02_breath": 2,
    "m04_foot": 3,
    "m05_portamento": 4,
    "m07_volume": 5,
    "m10_pan": 6,
    "m11_expression": 7,
    "m64_hold": 8,
    "m65_portamento": 9,
    "m66_sostenuto": 10,
    "m67_soft": 11,
    "m68_legato": 12,
    "m71_resonance": 13,
    "m74_frequency": 14,
    "m91_reverb": 15,
    "m93_chorus": 16,
    "custom_01": 17,
    "custom_02": 18,
    "custom_03": 19,
    "custom_04": 20,
    "custom_05": 21,
    "custom_06": 22,
    "custom_07": 23,
    "custom_08": 24,
    "keyswitch": 25,
}

MidiControlTarget = Literal[
    "m01_modulation",
    "m02_breath",
    "m04_foot",
    "m05_portamento",
    "m07_volume",
    "m10_pan",
    "m11_expression",
    "m64_hold",
    "m65_portamento",
    "m66_sostenuto",
    "m67_soft",
    "m68_legato",
    "m71_resonance",
    "m74_frequency",
    "m91_reverb",
    "m93_chorus",
    "custom_01",
    "custom_02",
    "custom_03",
    "custom_04",
    "custom_05",
    "custom_06",
    "custom_07",
    "custom_08",
    "keyswitch",
]


class CustomBankKnob(BaseModel):
    """
    Represents a knob in a custom bank with a name and control target.
    """

    name: str = ""
    control_target: MidiControlTarget | None = None


class CustomBank(BaseModel):
    """
    Represents a custom bank configuration with visibility and multiple knobs.
    """

    custom_bank_visible: bool = True
    knob_01: CustomBankKnob = Field(default_factory=CustomBankKnob)
    knob_02: CustomBankKnob = Field(default_factory=CustomBankKnob)
    knob_03: CustomBankKnob = Field(default_factory=CustomBankKnob)
    knob_04: CustomBankKnob = Field(default_factory=CustomBankKnob)
    knob_05: CustomBankKnob = Field(default_factory=CustomBankKnob)
    knob_06: CustomBankKnob = Field(default_factory=CustomBankKnob)
    knob_07: CustomBankKnob = Field(default_factory=CustomBankKnob)
    knob_08: CustomBankKnob = Field(default_factory=CustomBankKnob)

    def to_ksem_config(self) -> KsemCustomBank:
        """
        Converts the CustomBank instance to a KsemCustomBank configuration.
        """
        out = cast(
            KsemCustomBank,
            {"showHideCustomBank": int(self.custom_bank_visible), "label": {}},
        )
        for field_name in self.model_fields:
            if not field_name.startswith("knob"):
                continue

            field = getattr(self, field_name)
            number = int(field_name.split("_")[1])
            out[f"ctrl{number}_menu"] = (
                midi_control_to_ksem_custom_bank_selection[field.control_target]
                if field.control_target is not None
                else "-"
            )
            out["label"][f"ctrl{number}"] = field.name

        return out


class MetaSettings(BaseModel):
    """
    Represents meta settings for an instrument or product configuration.
    """

    comment_template: str | None = None
    colors: dict[str, str] | None = None
    middle_c: Literal["C3", "C4", "C5"] = "C3"

    midi_controls: MidiControls | None = None
    custom_bank: CustomBank | None = None


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

# Mapping of keyswitch fields to KSEM keys
keyswitch_field_to_ksem_key = {
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
    values: list[list[Note | str | int]]

    def to_ksem_config(self, settings: MetaSettings) -> dict[str, KsemKeyswitchesEntry]:
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
                else:
                    row_out[ksem_key] = value

            out[str(row_idx + 1)] = row_out

        return out


class Instrument(BaseModel):
    """
    Represents an instrument with meta settings and keyswitches.
    """

    meta_settings: MetaSettings = Field(default_factory=MetaSettings)
    keyswitches: Keyswitches


class InstrumentGroup(BaseModel):
    """
    Represents a group of instruments with shared meta settings.
    """

    meta_settings: MetaSettings = Field(default_factory=MetaSettings)
    instruments: dict[str, Instrument]


class Product(BaseModel):
    """
    Represents a product with meta settings and instrument groups.
    """

    meta_settings: MetaSettings = Field(default_factory=MetaSettings)
    instrument_groups: dict[str, InstrumentGroup]


@attrs.define()
class KsemConfigFile:
    """
    Represents a KSEM configuration file with its path and data.
    """

    file: Path
    data: KsemConfig


def _combine_dicts[K, V](*dicts: dict[K, V]) -> dict[K, V]:
    """
    Combines multiple dictionaries into one, prioritizing non-None values.
    """
    out: dict[K, V] = {}
    for dict_ in dicts:
        for k, v in dict_.items():
            if k not in out or v is not None:
                out[k] = v
    return out


class Root(BaseModel):
    """
    Represents the root configuration containing meta settings and products.
    """

    meta_settings: MetaSettings = Field(default_factory=MetaSettings)
    products: dict[str, Product]

    @classmethod
    def from_file(cls, file: Path) -> Root:
        """
        Loads a Root configuration from a YAML file.
        """
        with file.open() as f:
            data = yaml.load(f, Loader=yaml.Loader)
        return Root.model_validate(data)

    def write_ksem_config_files(self, root_dir: Path) -> None:
        """
        Writes KSEM configuration files to the specified root directory.
        """
        for config in self.to_ksem_configs():
            file = root_dir / config.file
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(json.dumps(config.data, indent=2))

    def to_ksem_configs(self) -> list[KsemConfigFile]:
        """
        Converts the Root configuration to a list of KsemConfigFile instances.
        """
        out: list[KsemConfigFile] = []

        for product_name, product in self.products.items():
            for group_name, group in product.instrument_groups.items():
                for instrument_name, instrument in group.instruments.items():
                    file = Path(product_name, group_name, f"{instrument_name}.json")
                    settings = MetaSettings.model_validate(
                        _combine_dicts(
                            self.meta_settings.model_dump(),
                            product.meta_settings.model_dump(),
                            group.meta_settings.model_dump(),
                            instrument.meta_settings.model_dump(),
                        )
                    )
                    if settings.midi_controls is None:
                        raise ValueError(
                            "`midi_controls` must be exist on a `meta_settings` object "
                            "in the hierarchy"
                        )
                    if settings.custom_bank is None:
                        raise ValueError(
                            "`custom_bank` must be exist on a `meta_settings` object "
                            "in the hierarchy"
                        )

                    ksem_config: KsemConfig = {
                        "KSEM-Version": float(KSEM_VERSION),
                        "ks": instrument.keyswitches.to_ksem_config(settings),
                        "midiControls": settings.midi_controls.to_ksem_config(),
                        "customBank": settings.custom_bank.to_ksem_config(),
                        "keySwitchSettings": {"keySwitchAmount": 1, "sendMainKey": 1},
                        "xyFade": {
                            "chooseXFade": 3,
                            "chooseYFade": 13,
                            "xyFadeShape": 0,
                            "yOrientation": 0,
                        },
                        "delaySettings": {
                            "usageRack": 0.0,
                            "filterMIDICtrl": 0.0,
                            "bufferSize": 3.0,
                            "delayCompensation": 0.0,
                            "lock": 1.0,
                            "delayBank": 0.0,
                            "delaySub": 0.1,
                            "delayPgm": 0.2,
                            "delayCC": 0.3,
                            "delayMainKey": 0.5,
                            "delayAdditionalKey": 0.6,
                            "delayMIDINote": 1.0,
                        },
                        "automationSettings": {
                            "automationKeySetting": 0,
                            "ignoreRepeatedKey": 1,
                            "autoTrigger": 0,
                            "protectAutomation": 0,
                        },
                        "keySwitchManager": {
                            "routerTrack": 1,
                            "routerFilter": 0,
                            "mpeSupportButton": 1,
                        },
                        "piano": {
                            "showHidePiano": 1,
                            "pitchLow": 55,
                            "pitchHigh": 106,
                            "automationKey": 108,
                        },
                        "pad": {
                            "fontSize": [0, 0, 1],
                            "justification": 0,
                            "showKSNumbers": 1,
                            "showKSNotes": 0,
                            "fontSizeButton": 0,
                        },
                        "comments": (
                            settings.comment_template.format(
                                product=product_name,
                                instrument_group=group_name,
                                instrument=instrument_name,
                            )
                            if settings.comment_template
                            else ""
                        ),
                    }

                    out.append(KsemConfigFile(file=file, data=ksem_config))
        return out


if __name__ == "__main__":
    # Load the root configuration from a YAML file and write KSEM config files
    loaded = Root.from_file(
        Path(
            r"H:\Libraries\Documents\_code\audio\ksem-transpiler\ksem_transpiler\example.yaml"
        )
    )
    print(
        loaded.write_ksem_config_files(
            Path(r"H:\Libraries\Documents\_code\audio\ksem-transpiler\output")
        )
    )
