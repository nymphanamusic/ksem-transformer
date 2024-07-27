from __future__ import annotations

from typing import Literal, get_args

from pydantic import BaseModel

from ksem_transformer.models.ksem_json_types import KsemConfig, KsemDelaySettings

type BufferSize = Literal[64, 128, 256, 512, 1024, 2048]
type DelayMode = Literal["compensation", "track_delay"]


class Delay(BaseModel):
    using_rack: bool = False
    chain_selector_filters_midi_control: bool = False
    buffer_size: BufferSize = 512

    delay_mode: DelayMode = "compensation"

    lock_midi_control_order: bool = True

    delay_bank: float = 0.0
    delay_sub: float = 0.1
    delay_program: float = 0.2
    delay_cc: float = 0.3
    delay_main_key: float = 0.5
    delay_second_key: float = 0.6
    delay_passed_thru_midi_note: float = 1.0

    @classmethod
    def from_ksem_config(cls, config: KsemConfig) -> Delay:
        cfg = config["delaySettings"]
        return Delay(
            using_rack=bool(cfg["usageRack"]),
            chain_selector_filters_midi_control=bool(cfg["filterMIDICtrl"]),
            buffer_size=get_args(BufferSize.__value__)[int(cfg["bufferSize"])],
            delay_mode=get_args(DelayMode.__value__)[int(cfg["delayCompensation"])],
            lock_midi_control_order=bool(cfg["lock"]),
            delay_bank=cfg["delayBank"],
            delay_sub=cfg["delaySub"],
            delay_program=cfg["delayPgm"],
            delay_cc=cfg["delayCC"],
            delay_main_key=cfg["delayMainKey"],
            delay_second_key=cfg["delayAdditionalKey"],
            delay_passed_thru_midi_note=cfg["delayMIDINote"],
        )

    def to_ksem_config(self) -> KsemDelaySettings:
        return {
            "usageRack": float(self.using_rack),
            "filterMIDICtrl": float(self.chain_selector_filters_midi_control),
            "bufferSize": float(get_args(BufferSize.__value__).index(self.buffer_size)),
            "delayCompensation": float(
                get_args(DelayMode.__value__).index(self.delay_mode)
            ),
            "lock": float(self.lock_midi_control_order),
            "delayBank": self.delay_bank,
            "delaySub": self.delay_sub,
            "delayPgm": self.delay_program,
            "delayCC": self.delay_cc,
            "delayMainKey": self.delay_main_key,
            "delayAdditionalKey": self.delay_second_key,
            "delayMIDINote": self.delay_passed_thru_midi_note,
        }
