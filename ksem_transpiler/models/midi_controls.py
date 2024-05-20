from typing import cast

from pydantic import BaseModel

from ksem_transpiler.models.ksem_json_types import KsemMidiControls

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


class MidiControl(BaseModel):
    """
    Represents a MIDI control with its enabled state, value, and optional MIDI CC number.
    """

    enabled: bool
    value: int
    midi_cc: int | None = None


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
