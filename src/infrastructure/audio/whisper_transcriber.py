import os
from typing import List

from faster_whisper import WhisperModel

from src.application.ports.transcriber import ITranscriber
from src.domain.entities.transcript import TranscriptDTO, TranscriptSegment


class WhisperTranscriber(ITranscriber):
    def __init__(self) -> None:
        model_size = os.getenv("WHISPER_MODEL", "small")
        compute_type = os.getenv("WHISPER_COMPUTE_TYPE", "int8")  # CPU-friendly
        download_root = os.getenv("WHISPER_CACHE_DIR", None)  # use default cache if None

        # Guardar o nome do modelo para report no DTO
        self._model_name = model_size

        self._model = WhisperModel(
            model_size,
            device="cpu",
            compute_type=compute_type,
            download_root=download_root,
        )

    def transcribe(self, file_path: str) -> TranscriptDTO:
        # Parâmetros conservadores para CPU, pt-BR, com VAD
        segments_iter, info = self._model.transcribe(
            file_path,
            language=os.getenv("WHISPER_LANGUAGE", "pt"),
            vad_filter=True,
            vad_parameters={"min_silence_duration_ms": 500},
            beam_size=int(os.getenv("WHISPER_BEAM_SIZE", "1")),
        )

        segments: List[TranscriptSegment] = []
        texts: List[str] = []
        for seg in segments_iter:
            segments.append(
                TranscriptSegment(start_s=float(seg.start), end_s=float(seg.end), text=seg.text)
            )
            texts.append(seg.text)

        dto = TranscriptDTO(
            interaction_id=None,
            language=info.language,
            model=f"faster-whisper:{self._model_name}",
            text=" ".join(texts).strip(),
            segments=segments,
        )
        return dto
