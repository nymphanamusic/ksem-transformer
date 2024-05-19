from __future__ import annotations

import re
from typing import Literal, cast

import attrs
from attr import Attribute
from attrs import field

type NoteLiteral = Literal[
    "C",
    "C#",
    "Db",
    "D",
    "D#",
    "Eb",
    "E",
    "F",
    "F#",
    "Gb",
    "G",
    "G#",
    "Ab",
    "A",
    "A#",
    "Bb",
    "B",
]
type MiddleCLiteral = Literal["C3", "C4", "C5"]


def _validate_note(
    instance: Note, attribute: Attribute[NoteLiteral], value: NoteLiteral
) -> None:
    if not re.match(r"[CDFGA]#?|[DEGAB]b?", value):
        raise ValueError(
            f'{value} is not a valid note. Try something like "C", "Bb", F#.'
        )


def _validate_octave(instance: Note, attribute: Attribute[int], value: int):
    match instance.middle_c:
        case "C3":
            lowest_octave, highest_octave = (-2, 8)
        case "C4":
            lowest_octave, highest_octave = (-1, 9)
        case "C5":
            lowest_octave, highest_octave = (0, 10)

    if value < lowest_octave or value > highest_octave:
        raise ValueError(
            f"Octave {value} is outside the allowed range [{lowest_octave}, "
            f"{highest_octave}] for middle C == {instance.middle_c}"
        )


@attrs.define()
class Note:
    note: NoteLiteral = field(validator=_validate_note)
    octave: int = field(validator=_validate_octave)
    middle_c: MiddleCLiteral = "C3"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Note):
            return self.to_midi() == other.to_midi()
        if isinstance(other, str):
            try:
                return self.to_midi() == Note.from_str(other).to_midi()
            except ValueError:
                pass
        return NotImplemented

    @classmethod
    def from_str(cls, value: str, middle_c: MiddleCLiteral = "C3") -> Note:
        if not (
            match_ := re.match(
                r"^(?P<note>[CDFGA]#?|[DEGAB]b?)(?P<octave>-[21]|\d|10)$", value
            )
        ):
            raise ValueError(f"{value} is not a valid note")

        note = cast(NoteLiteral, match_["note"])
        octave = int(match_["octave"])
        return Note(note, octave, middle_c=middle_c)

    @classmethod
    def from_midi(cls, midi: int, middle_c: MiddleCLiteral = "C3") -> Note:
        midi_to_key: dict[int, NoteLiteral] = {
            0: "C",
            1: "C#",
            # 1: "Db",
            2: "D",
            # 3: "D#",
            3: "Eb",
            4: "E",
            5: "F",
            6: "F#",
            # 6: "Gb",
            7: "G",
            8: "G#",
            # 8: "Ab",
            9: "A",
            # 10: "A#",
            10: "Bb",
            11: "B",
        }

        note = midi_to_key[midi % 12]
        octave = midi // 12
        return Note(note=note, octave=octave, middle_c=middle_c)

    def to_midi(self) -> int:
        lowest_octave_number = {"C3": 2, "C4": 1, "C5": 0}
        key_map = {
            "C": 0,
            "C#": 1,
            "Db": 1,
            "D": 2,
            "D#": 3,
            "Eb": 3,
            "E": 4,
            "F": 5,
            "F#": 6,
            "Gb": 6,
            "G": 7,
            "G#": 8,
            "Ab": 8,
            "A": 9,
            "A#": 10,
            "Bb": 10,
            "B": 11,
        }

        return (
            12 * (self.octave + lowest_octave_number[self.middle_c])
            + key_map[self.note]
        )
