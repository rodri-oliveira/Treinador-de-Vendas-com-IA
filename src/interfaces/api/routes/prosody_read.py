from fastapi import APIRouter, HTTPException, status

from src.infrastructure.db.sqlite import SessionLocal
from src.infrastructure.db import models as db_models
from src.interfaces.api.schemas import ProsodyResponse

router = APIRouter()


@router.get("/{interaction_id}", response_model=ProsodyResponse)
def get_prosody(interaction_id: str):
    session = SessionLocal()
    try:
        pr = (
            session.query(db_models.ProsodyFeatures)
            .filter(db_models.ProsodyFeatures.interaction_id == interaction_id)
            .one_or_none()
        )
        if pr is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prosody not found")

        return ProsodyResponse(
            duration_s=pr.duration_s,
            rms_mean=pr.rms_mean,
            rms_std=pr.rms_std,
            zcr_mean=pr.zcr_mean,
            zcr_std=pr.zcr_std,
            f0_mean=pr.f0_mean,
            f0_std=pr.f0_std,
        )
    finally:
        session.close()
