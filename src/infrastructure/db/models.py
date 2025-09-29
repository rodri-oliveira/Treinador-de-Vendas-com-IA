from __future__ import annotations
from sqlalchemy import Column, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from datetime import datetime

from .sqlite import Base


class Transcript(Base):
    __tablename__ = "transcripts"

    interaction_id = Column(String, primary_key=True, index=True)
    language = Column(String, nullable=True)
    model = Column(String, nullable=True)
    text = Column(Text, nullable=False)
    segments = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    prosody = relationship("ProsodyFeatures", back_populates="transcript", uselist=False, cascade="all, delete-orphan")


class ProsodyFeatures(Base):
    __tablename__ = "prosody_features"

    interaction_id = Column(String, ForeignKey("transcripts.interaction_id"), primary_key=True)
    duration_s = Column(Float, nullable=False)
    rms_mean = Column(Float, nullable=True)
    rms_std = Column(Float, nullable=True)
    zcr_mean = Column(Float, nullable=True)
    zcr_std = Column(Float, nullable=True)
    f0_mean = Column(Float, nullable=True)
    f0_std = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    transcript = relationship("Transcript", back_populates="prosody")
