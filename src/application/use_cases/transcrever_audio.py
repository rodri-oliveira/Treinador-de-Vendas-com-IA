from src.application.ports.transcriber import ITranscriber
from src.domain.entities.transcript import TranscriptDTO


class TranscreverAudio:
    """
    Caso de uso para transcrever um arquivo de áudio local utilizando a porta ITranscriber.
    Mantém orquestração fora das camadas de Interface e Infraestrutura.
    """

    def __init__(self, transcriber: ITranscriber) -> None:
        self._transcriber = transcriber

    def execute(self, file_path: str) -> TranscriptDTO:
        return self._transcriber.transcribe(file_path)
