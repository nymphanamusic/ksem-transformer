import pytest

from ksem_transformer.note import Note


class TestFromStr:
    def test_from_str_C3(self):
        assert Note.from_str("C3", middle_c="C3") == Note("C", 3, middle_c="C3")

    def test_from_str_Csharp3(self):
        assert Note.from_str("C#3", middle_c="C3") == Note("C#", 3, middle_c="C3")

    def test_from_str_Cneg1(self):
        assert Note.from_str("C-1", middle_c="C3") == Note("C", -1, middle_c="C3")

    def test_from_str_C10(self):
        assert Note.from_str("C10", middle_c="C5") == Note("C", 10, middle_c="C5")

    def test_from_str_middle_c(self):
        assert Note.from_str("C3", middle_c="C5") == Note("C", 3, middle_c="C5")


class TestEquality:
    def test_equivalence(self):
        assert Note("C", 3, middle_c="C3") == Note("C", 3, middle_c="C3")

    def test_inequivalence(self):
        assert Note("C", 3, middle_c="C3") != Note("C#", 3, middle_c="C3")

    def test_different_middle_C_dont_equate(self):
        assert Note("C", 3, middle_c="C3") != Note("C", 3, middle_c="C4")

    def test_Fsharp_eq_Gb(self):
        assert Note("F#", 3, middle_c="C3") == Note("Gb", 3, middle_c="C3")

    def test_equivalence_to_string(self):
        assert Note("C", 3, middle_c="C3") == "C3"


class TestToMidi:
    def test_middle_C_C3(self):
        assert Note("C", -2, middle_c="C3").to_midi() == 0

    def test_middle_C_C4(self):
        assert Note("C", -1, middle_c="C4").to_midi() == 0

    def test_middle_C_C5(self):
        assert Note("C", 0, middle_c="C5").to_midi() == 0

    def test_C3_and_middle_C_C3_is_midi_60(self):
        assert Note("C", 3, middle_c="C3").to_midi() == 60

    def test_G3_and_middle_C_C3_is_midi_67(self):
        assert Note("G", 3, middle_c="C3").to_midi() == 67

    def test_Fsharp_eq_Gb(self):
        assert (
            Note("F#", 3, middle_c="C3").to_midi()
            == Note("Gb", 3, middle_c="C3").to_midi()
        )


class TestFromMidi:
    def test_C_note(self):
        assert Note.from_midi(60, middle_c="C5").note == "C"

    def test_Fsharp_note(self):
        assert Note.from_midi(66, middle_c="C5").note == "F#"

    def test_B_note(self):
        assert Note.from_midi(71, middle_c="C5").note == "B"

    def test_B4_octave(self):
        assert Note.from_midi(59, middle_c="C5").octave == 4

    def test_C5_octave(self):
        assert Note.from_midi(60, middle_c="C5").octave == 5

    def test_middle_C_doesnt_alter_note(self):
        assert Note.from_midi(66, middle_c="C4").note == "F#"

    def test_middle_C_octave_invariance(self):
        assert (
            Note.from_midi(60, middle_c="C3").octave
            == Note.from_midi(60, middle_c="C4").octave
        )


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
