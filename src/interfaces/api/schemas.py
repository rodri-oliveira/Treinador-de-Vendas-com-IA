from typing import List, Optional
from pydantic import BaseModel


class ProsodyResponse(BaseModel):
    duration_s: float
    rms_mean: Optional[float] = None
    rms_std: Optional[float] = None
    zcr_mean: Optional[float] = None
    zcr_std: Optional[float] = None
    f0_mean: Optional[float] = None
    f0_std: Optional[float] = None


class TranscriptSegmentSchema(BaseModel):
    start_s: float
    end_s: float
    text: str


class TranscriptResponse(BaseModel):
    interaction_id: Optional[str] = None
    language: Optional[str] = None
    model: Optional[str] = None
    text: str
    segments: List[TranscriptSegmentSchema]

    # Campos opcionais de métricas e prosódia
    transcription_ms: Optional[int] = None
    prosody: Optional[ProsodyResponse] = None
    prosody_ms: Optional[int] = None
