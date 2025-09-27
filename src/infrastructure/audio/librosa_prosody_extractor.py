from src.application.ports.prosody_extractor import IProsodyExtractor
from src.domain.entities.prosody import ProsodyFeaturesDTO


class LibrosaProsodyExtractor(IProsodyExtractor):
    def extract(self, file_path: str) -> ProsodyFeaturesDTO:
        """Placeholder: implementação virá em etapa posterior usando librosa.
        Por ora, levantamos NotImplementedError para manter o contrato e a arquitetura.
        """
        raise NotImplementedError("LibrosaProsodyExtractor.extract ainda não implementado")
