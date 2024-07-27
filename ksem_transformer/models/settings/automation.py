from __future__ import annotations

from typing import Literal, get_args

from pydantic import BaseModel, ConfigDict

from ksem_transformer.models.ksem_json_types import KsemAutomationSettings, KsemConfig
from ksem_transformer.models.note_field import NoteField
from ksem_transformer.note import MiddleCLiteral, Note

type AutomationKeyResets = Literal["only_this_track", "all_ksem_instances"]


class Automation(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    automation_key: NoteField = Note.from_str("C7")
    automation_key_resets: AutomationKeyResets = "only_this_track"
    ignore_keyswitch_notes_in_midi_clips: bool = True
    trigger_keyswitch_on_armed_recording_start: bool = False
    pressing_keyswitches_affects_automation: bool = False

    @classmethod
    def from_ksem_config(
        cls, config: KsemConfig, middle_c: MiddleCLiteral
    ) -> Automation:
        cfg = config["automationSettings"]
        return Automation(
            automation_key=Note.from_midi(
                config["piano"]["automationKey"], middle_c=middle_c
            ),
            automation_key_resets=get_args(AutomationKeyResets.__value__)[
                cfg["automationKeySetting"]
            ],
            ignore_keyswitch_notes_in_midi_clips=bool(cfg["ignoreRepeatedKey"]),
            trigger_keyswitch_on_armed_recording_start=bool(cfg["autoTrigger"]),
            pressing_keyswitches_affects_automation=not bool(cfg["protectAutomation"]),
        )

    def to_ksem_config(self) -> KsemAutomationSettings:
        return {
            "automationKeySetting": get_args(AutomationKeyResets.__value__).index(
                self.automation_key_resets
            ),
            "ignoreRepeatedKey": int(self.ignore_keyswitch_notes_in_midi_clips),
            "autoTrigger": int(self.trigger_keyswitch_on_armed_recording_start),
            "protectAutomation": int(not self.pressing_keyswitches_affects_automation),
        }
