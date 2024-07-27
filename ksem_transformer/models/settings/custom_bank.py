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
)
type MidiControlTarget = Literal[
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

    @classmethod
    def from_ksem_config(cls, config: KsemConfig) -> CustomBank:
        cfg = config["customBank"]
        return CustomBank(
            custom_bank_visible=bool(cfg["showHideCustomBank"]),
            knob_01=CustomBankKnob(
                name=cfg["label"]["ctrl1"],
                control_target=cast(
                    MidiControlTarget,
                    midi_control_to_ksem_custom_bank_selection.inv[cfg["ctrl1_menu"]],
                ),
            ),
            knob_02=CustomBankKnob(
                name=cfg["label"]["ctrl2"],
                control_target=cast(
                    MidiControlTarget,
                    midi_control_to_ksem_custom_bank_selection.inv[cfg["ctrl2_menu"]],
                ),
            ),
            knob_03=CustomBankKnob(
                name=cfg["label"]["ctrl3"],
                control_target=cast(
                    MidiControlTarget,
                    midi_control_to_ksem_custom_bank_selection.inv[cfg["ctrl3_menu"]],
                ),
            ),
            knob_04=CustomBankKnob(
                name=cfg["label"]["ctrl4"],
                control_target=cast(
                    MidiControlTarget,
                    midi_control_to_ksem_custom_bank_selection.inv[cfg["ctrl4_menu"]],
                ),
            ),
            knob_05=CustomBankKnob(
                name=cfg["label"]["ctrl5"],
                control_target=cast(
                    MidiControlTarget,
                    midi_control_to_ksem_custom_bank_selection.inv[cfg["ctrl5_menu"]],
                ),
            ),
            knob_06=CustomBankKnob(
                name=cfg["label"]["ctrl6"],
                control_target=cast(
                    MidiControlTarget,
                    midi_control_to_ksem_custom_bank_selection.inv[cfg["ctrl6_menu"]],
                ),
            ),
            knob_07=CustomBankKnob(
                name=cfg["label"]["ctrl7"],
                control_target=cast(
                    MidiControlTarget,
                    midi_control_to_ksem_custom_bank_selection.inv[cfg["ctrl7_menu"]],
                ),
            ),
            knob_08=CustomBankKnob(
                name=cfg["label"]["ctrl8"],
                control_target=cast(
                    MidiControlTarget,
                    midi_control_to_ksem_custom_bank_selection.inv[cfg["ctrl8_menu"]],
                ),
            ),
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
