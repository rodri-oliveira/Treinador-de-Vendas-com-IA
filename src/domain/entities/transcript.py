from typing import List, Optional
from pydantic import BaseModel


class TranscriptSegment(BaseModel):
    start_s: float
    end_s: float
    text: str


class TranscriptDTO(BaseModel):
    interaction_id: Optional[str] = None
    language: Optional[str] = None
    model: Optional[str] = None
    text: str
    segments: List[TranscriptSegment] = []
