from abc import ABC, abstractmethod
from typing import Protocol
from src.domain.entities.transcript import TranscriptDTO


class ITranscriber(Protocol):
    @abstractmethod
    def transcribe(self, file_path: str) -> TranscriptDTO:
        """Transcreve um arquivo de áudio local e retorna um TranscriptDTO."""
        raise NotImplementedError
