from __future__ import annotations

from typing import Literal, cast

from bidict import bidict
from pydantic import BaseModel, Field

from ksem_transformer.models.ksem_json_types import KsemConfig, KsemCustomBank

# Mapping of internal MIDI control names to custom bank selection indices
midi_control_to_ksem_custom_bank_selection = bidict(
    {
        "m01_modulation": 1,
        "m02_breath": 2,
        "m04_foot_pedal": 3,
        "m05_portamento_time": 4,
        "m07_volume": 5,
        "m10_pan": 6,
        "m11_expression": 7,
        "m64_hold_pedal": 8,
        "m65_portamento_on_off": 9,
        "m66_sostenuto_pedal": 10,
        "m67_soft_pedal": 11,
        "m68_legato_pedal": 12,
        "m71_resonance": 13,
        "m74_frequency_cutoff": 14,
        "m91_reverb_level": 15,
        "m93_chorus_level": 16,
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
)
type MidiControlTarget = Literal[
    "m01_modulation",
    "m02_breath",
    "m04_foot_pedal",
    "m05_portamento_time",
    "m07_volume",
    "m10_pan",
    "m11_expression",
    "m64_hold_pedal",
    "m65_portamento_on_off",
    "m66_sostenuto_pedal",
    "m67_soft_pedal",
    "m68_legato_pedal",
    "m71_resonance",
    "m74_frequency_cutoff",
    "m91_reverb_level",
    "m93_chorus_level",
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

    @classmethod
    def from_ksem_config(cls, config: KsemConfig) -> CustomBank:
        cfg = config["customBank"]
        return CustomBank(
            custom_bank_visible=bool(cfg["showHideCustomBank"]),
            **{
                f"knob_{i:02d}": CustomBankKnob(
                    name=cast(str, cfg["label"][f"ctrl{1}"]),
                    control_target=cast(
                        MidiControlTarget,
                        midi_control_to_ksem_custom_bank_selection.inv[
                            cfg[f"ctrl{i}_menu"]
                        ],
                    ),
                )
                for i in range(1, 9)
            },
        )

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
