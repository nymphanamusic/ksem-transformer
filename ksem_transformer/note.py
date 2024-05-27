from __future__ import annotations

import re
from contextlib import contextmanager
from typing import ClassVar, Literal, cast

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

offset_to_key: dict[int, NoteLiteral] = {
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

key_to_offset = {
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


def _validate_note(
    instance: Note, attribute: Attribute[NoteLiteral], value: NoteLiteral
) -> None:
    if not re.match(r"[CDFGA]#?|[DEGAB]b?", value):
        raise ValueError(
            f'{value} is not a valid note. Try something like "C", "Bb", F#.'
        )


def _validate_octave(instance: Note, attribute: Attribute[int], value: int) -> None:
    if instance.middle_c is not None:
        _validate_octave_raw(value, instance.middle_c)


def _validate_octave_raw(value: int, middle_c: MiddleCLiteral) -> None:
    match middle_c:
        case "C3":
            lowest_octave, highest_octave = (-2, 8)
        case "C4":
            lowest_octave, highest_octave = (-1, 9)
        case "C5":
            lowest_octave, highest_octave = (0, 10)

    if value < lowest_octave or value > highest_octave:
        raise ValueError(
            f"Octave {value} is outside the allowed range [{lowest_octave}, "
            f"{highest_octave}] for middle C == {middle_c}"
        )


@attrs.define(hash=True)
class Note:
    _cls_middle_c: ClassVar[MiddleCLiteral | None] = None

    note: NoteLiteral = field(validator=_validate_note)
    octave: int = field(validator=_validate_octave)
    middle_c: MiddleCLiteral | None = None

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Note):
            return self.to_midi() == other.to_midi()
        if isinstance(other, str):
            # In this case we must assume the string is using the same middle C
            try:
                return (
                    self.to_midi()
                    == Note.from_str(other, middle_c=self.middle_c).to_midi()
                )
            except ValueError:
                pass
        return NotImplemented

    def __str__(self) -> str:
        return f"{self.note}{self.octave}"

    def __gt__(self, other: Note) -> bool:
        return self.to_midi() > other.to_midi()

    def __lt__(self, other: Note) -> bool:
        return self.to_midi() < other.to_midi()

    @classmethod
    @contextmanager
    def with_middle_c(cls, middle_c: MiddleCLiteral):
        prev_middle_c = cls._cls_middle_c
        cls._cls_middle_c = middle_c
        yield
        cls._cls_middle_c = prev_middle_c

    @classmethod
    def from_str(cls, value: str, middle_c: MiddleCLiteral | None = None) -> Note:
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
    def from_midi(cls, midi: int, middle_c: MiddleCLiteral | None = None) -> Note:
        note = offset_to_key[midi % 12]
        octave = midi // 12
        return Note(note=note, octave=octave, middle_c=middle_c)

    def to_midi(self) -> int:
        if self.middle_c is not None:
            middle_c = self.middle_c
        elif Note._cls_middle_c is not None:
            middle_c = Note._cls_middle_c
        else:
            raise TypeError(
                "A naive Note cannot be converted to a MIDI value. Set `middle_c` on "
                "the instance or use the `Note.with_middle_c` context manager"
            )

        lowest_octave_number = {"C3": 2, "C4": 1, "C5": 0}
        return (
            12 * (self.octave + lowest_octave_number[middle_c])
            + key_to_offset[self.note]
        )
