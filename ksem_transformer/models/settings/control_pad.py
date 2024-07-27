from __future__ import annotations

from typing import Literal, get_args

from pydantic import BaseModel

from ksem_transformer.models.ksem_json_types import KsemConfig, KsemPad

type FontSize = Literal[1, 2, 3, 4]
type Justification = Literal["left", "center"]


class ControlPad(BaseModel):
    font_size: FontSize = 2
    justification: Justification = "center"
    show_ks_number: bool = True
    show_ks_note: bool = False

    @classmethod
    def from_ksem_config(cls, config: KsemConfig) -> ControlPad:
        cfg = config["pad"]
        return ControlPad(
            # This one is weird. The font size comes from the third element in the list
            font_size=get_args(FontSize.__value__)[cfg["fontSize"][2]],
            justification=get_args(Justification.__value__)[cfg["justification"]],
            show_ks_number=bool(cfg["showKSNumbers"]),
            show_ks_note=bool(cfg["showKSNotes"]),
        )

    def to_ksem_config(self) -> KsemPad:
        return {
            "fontSize": [0, 0, get_args(FontSize.__value__).index(self.font_size)],
            "justification": get_args(Justification.__value__).index(
                self.justification
            ),
            "showKSNumbers": int(self.show_ks_number),
            "showKSNotes": int(self.show_ks_note),
            "fontSizeButton": 0,  # I think this setting does nothing
        }
