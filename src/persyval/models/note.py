import uuid
from typing import NewType

from pydantic import BaseModel, Field

NoteUid = NewType("NoteUid", uuid.UUID)


class Note(BaseModel):
    uid: NoteUid = Field(default_factory=lambda: NoteUid(uuid.uuid7()))
    title: str
    content: str
