from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ksem_transformer.models.note_field import NoteField
from ksem_transformer.models.settings.automation import Automation
from ksem_transformer.models.settings.custom_bank import CustomBank
from ksem_transformer.models.settings.delay import Delay
from ksem_transformer.models.settings.midi_controls import MidiControls
from ksem_transformer.models.settings.router import Router
from ksem_transformer.models.settings.xy_pad import XYPad
from ksem_transformer.note import Note


class PitchRange(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    low: NoteField
    high: NoteField


class Settings(BaseModel):
    """
    Represents settings for an instrument or product configuration.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    comment_template: str = ""
    colors: dict[str, str] | None = None
    middle_c: Literal["C3", "C4", "C5"] = "C3"
    pitch_range: PitchRange = PitchRange(
        low=Note("C", -2, "C3"), high=Note("C", 8, "C3")
    )
    mpe_support: bool = False

    midi_controls: MidiControls = Field(default_factory=MidiControls)
    custom_bank: CustomBank = Field(default_factory=CustomBank)
    xy_pad: XYPad = Field(default_factory=XYPad)
    delay: Delay = Field(default_factory=Delay)
    automation: Automation = Field(default_factory=Automation)
    router: Router = Field(default_factory=Router)