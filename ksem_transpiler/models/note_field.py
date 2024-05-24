from typing import Annotated, Any

from pydantic import BeforeValidator, ValidationInfo

from ksem_transpiler.note import Note


def note_validator(v: Any, info: ValidationInfo) -> Note:
    if isinstance(v, Note):
        return v
    if isinstance(v, str):
        return Note.from_str(v)
    raise TypeError("value must be one of type [Note, str]")


NoteField = Annotated[Note, BeforeValidator(note_validator)]
