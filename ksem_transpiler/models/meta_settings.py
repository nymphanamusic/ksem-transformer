from typing import Literal

from pydantic import BaseModel

from ksem_transpiler.models.custom_bank import CustomBank
from ksem_transpiler.models.midi_controls import MidiControls


class MetaSettings(BaseModel):
    """
    Represents meta settings for an instrument or product configuration.
    """

    comment_template: str | None = None
    colors: dict[str, str] | None = None
    middle_c: Literal["C3", "C4", "C5"] = "C3"

    midi_controls: MidiControls | None = None
    custom_bank: CustomBank | None = None
