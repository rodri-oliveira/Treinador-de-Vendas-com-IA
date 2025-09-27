from typing import Optional
from pydantic import BaseModel


class ProsodyFeaturesDTO(BaseModel):
    duration_s: float
    rms_mean: Optional[float] = None
    rms_std: Optional[float] = None
    zcr_mean: Optional[float] = None
    zcr_std: Optional[float] = None
    f0_mean: Optional[float] = None
    f0_std: Optional[float] = None
