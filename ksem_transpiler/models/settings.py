from typing import Literal

from pydantic import BaseModel
from pydantic import BaseModel, ConfigDict, Field

from ksem_transpiler.models.custom_bank import CustomBank
from ksem_transpiler.models.midi_controls import MidiControls
from ksem_transpiler.models.note_field import NoteField
from ksem_transpiler.note import Note


class PitchRange(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    low: NoteField
    high: NoteField


class Settings(BaseModel):
    """
    Represents settings for an instrument or product configuration.
    """

    comment_template: str | None = None
    model_config = ConfigDict(arbitrary_types_allowed=True)

    colors: dict[str, str] | None = None
    middle_c: Literal["C3", "C4", "C5"] = "C3"
    pitch_range: PitchRange = PitchRange(
        low=Note("C", -2, "C3"), high=Note("C", 8, "C3")
    )
    automation_key: NoteField = Note.from_str("C8")

    midi_controls: MidiControls | None = None
    custom_bank: CustomBank | None = None
