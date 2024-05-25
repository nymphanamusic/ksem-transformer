from typing import Literal, get_args

from pydantic import BaseModel

from ksem_transformer.models.ksem_json_types import KsemAutomationSettings
from ksem_transformer.models.note_field import NoteField
from ksem_transformer.note import Note

AutomationKeyResets = Literal["only_this_track", "all_ksem_instances"]


class Automation(BaseModel):
    automation_key: NoteField = Note.from_str("C7")
    automation_key_resets: AutomationKeyResets = "only_this_track"
    ignore_keyswitch_notes_in_midi_clips: bool = True
    trigger_keyswitch_on_armed_recording_start: bool = False
    pressing_keyswitches_affects_automation: bool = False

    def to_ksem_config(self) -> KsemAutomationSettings:
        return {
            "automationKeySetting": get_args(AutomationKeyResets).index(
                self.automation_key_resets
            ),
            "ignoreRepeatedKey": int(self.ignore_keyswitch_notes_in_midi_clips),
            "autoTrigger": int(self.trigger_keyswitch_on_armed_recording_start),
            "protectAutomation": int(not self.pressing_keyswitches_affects_automation),
        }
