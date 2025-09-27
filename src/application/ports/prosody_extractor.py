from abc import ABC, abstractmethod
from typing import Protocol

from src.domain.entities.prosody import ProsodyFeaturesDTO


class IProsodyExtractor(Protocol):
    @abstractmethod
    def extract(self, file_path: str) -> ProsodyFeaturesDTO:
        """Extrai features de prosódia de um arquivo de áudio local."""
        raise NotImplementedError
