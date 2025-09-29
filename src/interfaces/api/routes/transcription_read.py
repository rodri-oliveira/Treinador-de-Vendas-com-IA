from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import joinedload

from src.infrastructure.db.sqlite import SessionLocal
from src.infrastructure.db import models as db_models
from src.interfaces.api.schemas import TranscriptResponse, ProsodyResponse

router = APIRouter()


@router.get("/{interaction_id}", response_model=TranscriptResponse)
def get_transcription(interaction_id: str):
    session = SessionLocal()
    try:
        tr = (
            session.query(db_models.Transcript)
            .options(joinedload(db_models.Transcript.prosody))
            .filter(db_models.Transcript.interaction_id == interaction_id)
            .one_or_none()
        )
        if tr is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transcription not found")

        segments = tr.segments or []
        data = {
            "interaction_id": tr.interaction_id,
            "language": tr.language,
            "model": tr.model,
            "text": tr.text,
            "segments": segments,
        }

        if tr.prosody:
            data["prosody"] = ProsodyResponse(
                duration_s=tr.prosody.duration_s,
                rms_mean=tr.prosody.rms_mean,
                rms_std=tr.prosody.rms_std,
                zcr_mean=tr.prosody.zcr_mean,
                zcr_std=tr.prosody.zcr_std,
                f0_mean=tr.prosody.f0_mean,
                f0_std=tr.prosody.f0_std,
            ).model_dump()

        return data
    finally:
        session.close()
