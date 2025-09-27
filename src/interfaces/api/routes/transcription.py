import os
import tempfile
import time
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Response

from src.application.use_cases.transcrever_audio import TranscreverAudio
from src.infrastructure.audio.whisper_transcriber import WhisperTranscriber
from src.infrastructure.audio.librosa_prosody_extractor import LibrosaProsodyExtractor
from src.interfaces.api.schemas import TranscriptResponse

router = APIRouter()

# Instâncias de longa duração (evita re-carregar modelos a cada request)
TRANSCRIBER_SINGLETON = WhisperTranscriber()
PROSODY_EXTRACTOR_SINGLETON = LibrosaProsodyExtractor(target_sr=16000)


@router.post("/upload", response_model=TranscriptResponse)
async def upload_audio(file: UploadFile = File(...), include_prosody: bool = False, resp: Response | None = None):
    # Validação de extensão
    allowed_ext = {"wav", "mp3", "m4a", "ogg"}
    filename = file.filename or ""
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    if ext not in allowed_ext:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Formato não suportado: {ext}. Suportados: {', '.join(sorted(allowed_ext))}",
        )

    # Persistir temporariamente para o transcritor consumir via caminho de arquivo
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
                detail=f"Arquivo excede o limite de {max_mb}MB"
            )

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=tmp_dir) as tmp:
            tmp_file = tmp.name
            tmp.write(content)

        use_case = TranscreverAudio(TRANSCRIBER_SINGLETON)

        req_start = time.perf_counter()
        t0 = req_start
        dto = use_case.execute(tmp_file)
        t1 = time.perf_counter()

        response_data = dto.model_dump()
        response_data["transcription_ms"] = int((t1 - t0) * 1000)

        if include_prosody:
            p0 = time.perf_counter()
            prosody = PROSODY_EXTRACTOR_SINGLETON.extract(tmp_file)
            p1 = time.perf_counter()
            response_data["prosody"] = prosody.model_dump()
            response_data["prosody_ms"] = int((p1 - p0) * 1000)

        if resp is not None:
            total_ms = int((time.perf_counter() - req_start) * 1000)
            resp.headers["X-Process-Time-ms"] = str(total_ms)

        return response_data

    except HTTPException:
        # Propagar HTTPException como está
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if tmp_file and os.path.exists(tmp_file):
            try:
                os.remove(tmp_file)
            except Exception:
                # Ignorar erro de limpeza
                pass
