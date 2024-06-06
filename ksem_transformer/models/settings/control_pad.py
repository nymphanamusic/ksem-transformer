from typing import Literal, get_args

from pydantic import BaseModel

from ksem_transformer.models.ksem_json_types import KsemPad

type FontSize = Literal[1, 2, 3, 4]
type Justification = Literal["left", "center"]


class ControlPad(BaseModel):
    font_size: FontSize = 2
    justification: Justification = "center"
    show_ks_number: bool = True
    show_ks_note: bool = False

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
