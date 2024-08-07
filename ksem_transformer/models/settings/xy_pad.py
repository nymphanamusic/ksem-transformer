from __future__ import annotations

import typing
from typing import Literal, cast, get_args

from pydantic import BaseModel

from ksem_transformer.models.ksem_json_types import KsemConfig, KsemXYFade

type AxisTarget = Literal[
    None,
    "velocity",
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
    37,
    38,
    39,
    40,
    41,
    42,
    43,
    44,
    45,
    46,
    47,
    48,
    49,
    50,
    51,
    52,
    53,
    54,
    55,
    56,
    57,
    58,
    59,
    60,
    61,
    62,
    63,
    64,
    65,
    66,
    67,
    68,
    69,
    70,
    71,
    72,
    73,
    74,
    75,
    76,
    77,
    78,
    79,
    80,
    81,
    82,
    83,
    84,
    85,
    86,
    87,
    88,
    89,
    90,
    91,
    92,
    93,
    94,
    95,
    96,
    97,
    98,
    99,
    100,
    101,
    102,
    103,
    104,
    105,
    106,
    107,
    108,
    109,
    110,
    111,
    112,
    113,
    114,
    115,
    116,
    117,
    118,
    119,
]
type PadShape = Literal["filled_rectangle", "line"]


class XYPad(BaseModel):
    x_axis_target: AxisTarget = None
    y_axis_target: AxisTarget = None
    pad_shape: PadShape = "filled_rectangle"

    @classmethod
    def from_ksem_config(cls, config: KsemConfig) -> XYPad:
        cfg = config["xyFade"]
        return XYPad(
            x_axis_target=cast(
                AxisTarget, get_args(AxisTarget.__value__)[cfg["chooseXFade"]]
            ),
            y_axis_target=cast(
                AxisTarget, get_args(AxisTarget.__value__)[cfg["chooseYFade"]]
            ),
            pad_shape=cast(PadShape, get_args(PadShape.__value__)[cfg["xyFadeShape"]]),
        )

    def to_ksem_config(self) -> KsemXYFade:
        axis_target_options = typing.get_args(AxisTarget.__value__)
        pad_shape_options = typing.get_args(PadShape.__value__)
        return {
            "chooseXFade": axis_target_options.index(self.x_axis_target),
            "chooseYFade": axis_target_options.index(self.y_axis_target),
            "xyFadeShape": pad_shape_options.index(self.pad_shape),
            "yOrientation": 0,
        }
