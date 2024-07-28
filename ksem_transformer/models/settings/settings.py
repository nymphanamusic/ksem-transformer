from __future__ import annotations

from copy import copy
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field

from ksem_transformer.models.ksem_json_types import KsemConfig
from ksem_transformer.models.note_field import NoteField
from ksem_transformer.models.settings.automation import Automation
from ksem_transformer.models.settings.control_pad import ControlPad
from ksem_transformer.models.settings.custom_bank import CustomBank
from ksem_transformer.models.settings.delay import Delay
from ksem_transformer.models.settings.midi_controls import MidiControls
from ksem_transformer.models.settings.router import Router
from ksem_transformer.models.settings.xy_pad import XYPad
from ksem_transformer.note import MiddleCLiteral, Note


class PitchRange(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    low: NoteField
    high: NoteField

    @classmethod
    def from_ksem_config(
        cls, config: KsemConfig, middle_c: MiddleCLiteral
    ) -> PitchRange:
        return PitchRange(
            low=Note.from_midi(config["piano"]["pitchLow"], middle_c=middle_c),
            high=Note.from_midi(config["piano"]["pitchHigh"], middle_c=middle_c),
        )


class Settings(BaseModel):
    """
    Represents settings for an instrument or product configuration.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    default_middle_c: ClassVar[MiddleCLiteral] = "C3"
    _default_pitch_range: ClassVar[PitchRange] = PitchRange(
        low=Note("C", -2, "C3"), high=Note("C", 8, "C3")
    )

    comment_template: str = ""
    colors: dict[str, str] = Field(default_factory=dict)
    middle_c: MiddleCLiteral = default_middle_c
    pitch_range: PitchRange = copy(_default_pitch_range)
    mpe_support: bool = False
    send_main_key: bool = True

    midi_controls: MidiControls = Field(default_factory=MidiControls)
    custom_bank: CustomBank = Field(default_factory=CustomBank)
    xy_pad: XYPad = Field(default_factory=XYPad)
    delay: Delay = Field(default_factory=Delay)
    automation: Automation = Field(default_factory=Automation)
    router: Router = Field(default_factory=Router)
    control_pad: ControlPad = Field(default_factory=ControlPad)

    @classmethod
    def default_pitch_range(cls) -> PitchRange:
        return copy(cls._default_pitch_range)

    def is_default(self) -> bool:
        return self == Settings()

    @classmethod
    def from_ksem_config(cls, config: KsemConfig) -> Settings:
        return Settings(
            pitch_range=PitchRange.from_ksem_config(config, cls.default_middle_c),
            mpe_support=bool(config["keySwitchManager"]["mpeSupportButton"]),
            send_main_key=bool(config["keySwitchSettings"]["sendMainKey"]),
            midi_controls=MidiControls.from_ksem_config(config),
            custom_bank=CustomBank.from_ksem_config(config),
            xy_pad=XYPad.from_ksem_config(config),
            delay=Delay.from_ksem_config(config),
            automation=Automation.from_ksem_config(config, cls.default_middle_c),
            router=Router.from_ksem_config(config),
            control_pad=ControlPad.from_ksem_config(config),
        )

    @classmethod
    def combine(cls, *others: Settings) -> Settings:
        default = Settings().model_dump()
        out: dict[str, Any] = {}
        for other in others:
            other_dumped = other.model_dump()
            for k, v in dict(other_dumped).items():
                # Remove all fields that are default values so they don't overwrite previous things
                if v == default[k]:
                    del other_dumped[k]
            out.update(other_dumped)
        # Any field not set in any of the object will be populated by the Settings
        # defaults
        return Settings.model_validate(out)
