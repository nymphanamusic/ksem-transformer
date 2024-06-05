from collections.abc import Sequence
from functools import cached_property
from typing import Never, cast, get_args

import attrs
import pytest
from hypothesis import given
from hypothesis import strategies as st

from ksem_transformer.note import MiddleCLiteral, Note, NoteLiteral

middle_c_octave_ranges = {"C3": (-2, 8), "C4": (-1, 9), "C5": (0, 10)}
flats_to_sharps: dict[NoteLiteral, NoteLiteral] = {
    "Db": "C#",
    "Eb": "D#",
    "Gb": "F#",
    "Ab": "G#",
    "Bb": "A#",
}

middle_cs = st.from_type(MiddleCLiteral.__value__)
notes = st.from_type(NoteLiteral.__value__)


@attrs.define
class NoteInfo:
    note: NoteLiteral
    octave: int
    middle_c: MiddleCLiteral

    def __eq__(self, _: object) -> Never:
        raise NotImplementedError("You probably meant to use `note_info.instance`!")

    @cached_property
    def instance(self) -> Note:
        return Note(self.note, self.octave, self.middle_c)


@st.composite
def valid_notes(
    draw: st.DrawFn,
    note_strategy: st.SearchStrategy[NoteLiteral] = notes,
    octave_strategy: st.SearchStrategy[int] | None = None,
    middle_c_strategy: st.SearchStrategy[MiddleCLiteral] = middle_cs,
) -> NoteInfo:
    note = draw(note_strategy)
    middle_c = draw(middle_c_strategy)

    if octave_strategy is not None:
        octave = draw(octave_strategy)
    else:
        octave_range = middle_c_octave_ranges[middle_c]
        octave = draw(st.integers(*octave_range))

    return NoteInfo(note, octave, middle_c)


flats = valid_notes(st.sampled_from(list(flats_to_sharps.keys())))


@st.composite
def sharps(draw: st.DrawFn) -> NoteInfo:
    flat_note_info = draw(st.shared(flats, key="sharps"))
    # Create the corresponding sharp note that is equivalent to this flat note
    return NoteInfo(
        flats_to_sharps[flat_note_info.note],
        flat_note_info.octave,
        flat_note_info.middle_c,
    )


@st.composite
def sharp_and_flat_equivalent_notes(draw: st.DrawFn) -> tuple[NoteInfo, NoteInfo]:

    sharp_note = draw(st.sampled_from(list(flats_to_sharps.keys())))
    flat_note = flats_to_sharps[sharp_note]

    middle_c = cast(MiddleCLiteral, draw(middle_cs))

    octave_range = middle_c_octave_ranges[middle_c]
    octave = draw(st.integers(*octave_range))

    return NoteInfo(flat_note, octave, middle_c), NoteInfo(sharp_note, octave, middle_c)


@given(valid_notes())
def test_from_str(note_info: NoteInfo):
    assert (
        Note.from_str(f"{note_info.note}{note_info.octave}", note_info.middle_c)
        == note_info.instance
    )


class TestEquality:
    @given(st.shared(flats, key="sharps"), sharps())
    def test_equivalent_sharps_and_flats(
        self, flat_note_info: NoteInfo, sharp_note_info: NoteInfo
    ):
        assert flat_note_info.instance == sharp_note_info.instance

    @given(valid_notes(), valid_notes())
    def test_equality_does_not_raise(
        self, note_info_1: NoteInfo, note_info_2: NoteInfo
    ):
        assert isinstance(note_info_1.instance == note_info_2.instance, bool)

    @given(valid_notes(), valid_notes())
    def test_equality_to_string_does_not_raise(
        self, note_info_1: NoteInfo, note_info_2: NoteInfo
    ):
        assert isinstance(
            note_info_1.instance == f"{note_info_2.note}{note_info_2.octave}", bool
        )

    @given(valid_notes())
    def test_equality_to_self_as_string_is_true(self, note_info: NoteInfo):
        assert note_info.instance == f"{note_info.note}{note_info.octave}"

    @given(
        notes, st.integers(0, 8), st.permutations(get_args(MiddleCLiteral.__value__))
    )
    def test_notes_with_different_middle_Cs_are_unequal(
        self, note: NoteLiteral, octave: int, middle_cs: Sequence[MiddleCLiteral]
    ):
        assert Note(note, octave, middle_cs[0]) != Note(note, octave, middle_cs[1])


@given(st.integers(0, 127), middle_cs)
def test_midi_roundtrip(midi: int, middle_c: MiddleCLiteral):
    assert Note.from_midi(midi, middle_c).to_midi() == midi


class TestNaiveNotes:
    def test_naive_note_to_aware_note(self):
        with Note.with_middle_c("C5"):
            assert Note("C", 0).to_midi() == 0

    def test_naive_note_to_midi_raises_exc(self):
        with pytest.raises(TypeError):
            Note("C", 2, middle_c=None).to_midi()

    def test_naive_note_exiting_context_raises_exc(self):
        with Note.with_middle_c("C5"):
            pass
        with pytest.raises(TypeError):
            Note("C", 2, middle_c=None).to_midi()

    def test_nesting_recovers_previous_contexts_value(self):
        with Note.with_middle_c("C4"):
            with Note.with_middle_c("C5"):
                assert Note("C", 0).to_midi() == 0
            assert Note("C", -1).to_midi() == 0
