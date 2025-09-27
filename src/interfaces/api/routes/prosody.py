import os
import tempfile
import time
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Response

from src.infrastructure.audio.librosa_prosody_extractor import LibrosaProsodyExtractor
from src.domain.entities.prosody import ProsodyFeaturesDTO
from src.interfaces.api.schemas import ProsodyResponse

router = APIRouter()

# Instância de longa duração
PROSODY_EXTRACTOR_SINGLETON = LibrosaProsodyExtractor(target_sr=16000)


@router.post("/extract", response_model=ProsodyResponse)
async def extract_prosody(file: UploadFile = File(...), response: Response = None):
    # Validação de extensão básica
    allowed_ext = {"wav", "mp3", "m4a", "ogg"}
    filename = file.filename or ""
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    if ext not in allowed_ext:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Formato não suportado: {ext}. Suportados: {', '.join(sorted(allowed_ext))}",
        )

    tmp_dir = os.getenv("TMP_AUDIO_DIR", None)
    tmp_file = None
    try:
        suffix = f".{ext}" if ext else ""
        # Garantir diretório temporário se definido via env
        if tmp_dir:
            os.makedirs(tmp_dir, exist_ok=True)

        # Ler conteúdo (limite de tamanho opcional via env)
        content = await file.read()
        max_mb = int(os.getenv("MAX_UPLOAD_MB", "50"))
        max_bytes = max_mb * 1024 * 1024
        if len(content) > max_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Arquivo excede o limite de {max_mb}MB",
            )

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=tmp_dir) as tmp:
            tmp_file = tmp.name
            tmp.write(content)

        start = time.perf_counter()
        dto: ProsodyFeaturesDTO = PROSODY_EXTRACTOR_SINGLETON.extract(tmp_file)
        if response is not None:
            response.headers["X-Process-Time-ms"] = str(int((time.perf_counter() - start) * 1000))
        return dto.model_dump()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if tmp_file and os.path.exists(tmp_file):
            try:
                os.remove(tmp_file)
            except Exception:
                pass
