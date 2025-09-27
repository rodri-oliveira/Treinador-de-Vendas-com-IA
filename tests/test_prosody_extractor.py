import os
import tempfile
import numpy as np
import soundfile as sf
import pytest

from src.infrastructure.audio.librosa_prosody_extractor import LibrosaProsodyExtractor


def test_librosa_prosody_extractor_on_sine_wave():
    # Gera seno 1s a 440Hz
    sr = 16000
    duration_s = 1.0
    t = np.linspace(0, duration_s, int(sr * duration_s), endpoint=False)
    y = (0.2 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        sf.write(tmp_path, y, sr)

        extractor = LibrosaProsodyExtractor(target_sr=sr)
        dto = extractor.extract(tmp_path)

        assert dto.duration_s == pytest.approx(duration_s, rel=0.05)
        assert dto.rms_mean is not None and dto.rms_mean > 0
        assert dto.zcr_mean is not None and dto.zcr_mean >= 0
        assert dto.f0_mean is None
        assert dto.f0_std is None
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
