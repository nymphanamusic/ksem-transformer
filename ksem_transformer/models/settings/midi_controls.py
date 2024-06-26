import typing
from typing import Literal, cast

from pydantic import BaseModel, Field

from ksem_transformer.models.ksem_json_types import KsemMidiControls

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

# Available MIDI CC KSEM options
type CustomOptions = Literal[
    0,
    3,
    6,
    8,
    9,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
    37,
    38,
    39,
    40,
    41,
    42,
    43,
    44,
    45,
    46,
    47,
    48,
    49,
    50,
    51,
    52,
    53,
    54,
    55,
    56,
    57,
    58,
    59,
    60,
    61,
    62,
    63,
    69,
    70,
    72,
    73,
    75,
    76,
    77,
    78,
    79,
    80,
    81,
    82,
    83,
    84,
    85,
    86,
    87,
    88,
    89,
    90,
    92,
    94,
    95,
    96,
    97,
    98,
    99,
    100,
    101,
    102,
    103,
    104,
    105,
    106,
    107,
    108,
    109,
    110,
    111,
    112,
    113,
    114,
    115,
    116,
    117,
    118,
    119,
]

custom_options = [None, *typing.get_args(CustomOptions.__value__)]


class MidiControl(BaseModel):
    """
    Represents a MIDI control with its enabled state, value, and optional MIDI CC number.
    """

    enabled: bool = False
    value: int = 0


class CustomMidiControl(MidiControl, BaseModel):
    midi_cc: CustomOptions | None = None


class MidiControls(BaseModel):
    """
    Represents a collection of MIDI controls.
    """

    m01_modulation: MidiControl = Field(default_factory=MidiControl)
    m02_breath: MidiControl = Field(default_factory=MidiControl)
    m04_foot: MidiControl = Field(default_factory=MidiControl)
    m05_portamento: MidiControl = Field(default_factory=MidiControl)
    m07_volume: MidiControl = Field(default_factory=MidiControl)
    m10_pan: MidiControl = Field(default_factory=MidiControl)
    m11_expression: MidiControl = Field(default_factory=MidiControl)
    m64_hold: MidiControl = Field(default_factory=MidiControl)
    m65_portamento: MidiControl = Field(default_factory=MidiControl)
    m66_sostenuto: MidiControl = Field(default_factory=MidiControl)
    m67_soft: MidiControl = Field(default_factory=MidiControl)
    m68_legato: MidiControl = Field(default_factory=MidiControl)
    m71_resonance: MidiControl = Field(default_factory=MidiControl)
    m74_frequency: MidiControl = Field(default_factory=MidiControl)
    m91_reverb: MidiControl = Field(default_factory=MidiControl)
    m93_chorus: MidiControl = Field(default_factory=MidiControl)

    custom_01: CustomMidiControl = Field(default_factory=CustomMidiControl)
    custom_02: CustomMidiControl = Field(default_factory=CustomMidiControl)
    custom_03: CustomMidiControl = Field(default_factory=CustomMidiControl)
    custom_04: CustomMidiControl = Field(default_factory=CustomMidiControl)
    custom_05: CustomMidiControl = Field(default_factory=CustomMidiControl)
    custom_06: CustomMidiControl = Field(default_factory=CustomMidiControl)
    custom_07: CustomMidiControl = Field(default_factory=CustomMidiControl)
    custom_08: CustomMidiControl = Field(default_factory=CustomMidiControl)

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
            if isinstance(field, CustomMidiControl):
                # Get the MIDI CC's option index (magic values in KSEM)
                out[f"{ksem_key}_num"] = custom_options.index(field.midi_cc)

        return out
