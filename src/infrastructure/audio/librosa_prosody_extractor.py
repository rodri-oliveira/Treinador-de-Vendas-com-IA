from __future__ import annotations

import librosa
import numpy as np

from src.application.ports.prosody_extractor import IProsodyExtractor
from src.domain.entities.prosody import ProsodyFeaturesDTO


class LibrosaProsodyExtractor(IProsodyExtractor):
    def __init__(self, target_sr: int = 16000) -> None:
        self._target_sr = target_sr

    def extract(self, file_path: str) -> ProsodyFeaturesDTO:
        # Carregar áudio mono e normalizado para target_sr (CPU-friendly)
        y, sr = librosa.load(file_path, sr=self._target_sr, mono=True)
        if y.size == 0:
            return ProsodyFeaturesDTO(
                duration_s=0.0,
                rms_mean=None,
                rms_std=None,
                zcr_mean=None,
                zcr_std=None,
                f0_mean=None,
                f0_std=None,
            )

        duration_s = float(len(y) / sr)

        # RMS (energia)
        rms = librosa.feature.rms(y=y)[0]
        rms_mean = float(np.mean(rms)) if rms.size else None
        rms_std = float(np.std(rms)) if rms.size else None

        # Zero-Crossing Rate (ZCR)
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        zcr_mean = float(np.mean(zcr)) if zcr.size else None
        zcr_std = float(np.std(zcr)) if zcr.size else None

        # F0 deixado como None no MVP (yin pode ser adicionado depois)
        f0_mean = None
        f0_std = None

        return ProsodyFeaturesDTO(
            duration_s=duration_s,
            rms_mean=rms_mean,
            rms_std=rms_std,
            zcr_mean=zcr_mean,
            zcr_std=zcr_std,
            f0_mean=f0_mean,
            f0_std=f0_std,
        )
