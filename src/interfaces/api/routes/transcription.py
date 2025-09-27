import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException, status

from src.application.use_cases.transcrever_audio import TranscreverAudio
from src.infrastructure.audio.whisper_transcriber import WhisperTranscriber

router = APIRouter()


@router.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
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
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=tmp_dir) as tmp:
            tmp_file = tmp.name
            content = await file.read()
            tmp.write(content)

        transcriber = WhisperTranscriber()
        use_case = TranscreverAudio(transcriber)
        dto = use_case.execute(tmp_file)
        return dto.model_dump()

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
