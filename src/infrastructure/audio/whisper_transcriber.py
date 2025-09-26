from src.application.ports.transcriber import ITranscriber
from src.domain.entities.transcript import TranscriptDTO


class WhisperTranscriber(ITranscriber):
    def transcribe(self, file_path: str) -> TranscriptDTO:
        """Placeholder de implementação. A lógica será adicionada em sprint futura.
        Aqui apenas levantamos um NotImplementedError para indicar etapa pendente.
        """
        raise NotImplementedError("WhisperTranscriber.transcribe ainda não implementado")
