import os
import tempfile
import time
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Response
import uuid
import logging

from src.application.use_cases.transcrever_audio import TranscreverAudio
from src.infrastructure.audio.whisper_transcriber import WhisperTranscriber
from src.infrastructure.audio.librosa_prosody_extractor import LibrosaProsodyExtractor
from src.interfaces.api.schemas import TranscriptResponse
from src.infrastructure.db.sqlite import SessionLocal
from src.infrastructure.db import models as db_models

router = APIRouter()

# Instâncias de longa duração (evita re-carregar modelos a cada request)
TRANSCRIBER_SINGLETON = WhisperTranscriber()
PROSODY_EXTRACTOR_SINGLETON = LibrosaProsodyExtractor(target_sr=16000)


@router.post("/upload", response_model=TranscriptResponse)
async def upload_audio(file: UploadFile = File(...), include_prosody: bool = False, response: Response = None):
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

        # Garante interaction_id
        if not dto.interaction_id:
            dto.interaction_id = str(uuid.uuid4())

        response_data = dto.model_dump()
        response_data["transcription_ms"] = int((t1 - t0) * 1000)

        if include_prosody:
            p0 = time.perf_counter()
            prosody = PROSODY_EXTRACTOR_SINGLETON.extract(tmp_file)
            p1 = time.perf_counter()
            response_data["prosody"] = prosody.model_dump()
            response_data["prosody_ms"] = int((p1 - p0) * 1000)

        if response is not None:
            total_ms = int((time.perf_counter() - req_start) * 1000)
            response.headers["X-Process-Time-ms"] = str(total_ms)

        # Logs estruturados mínimos
        try:
            logging.getLogger(__name__).info(
                "transcription_done",
                extra={
                    "interaction_id": dto.interaction_id,
                    "file_size_bytes": len(content),
                    "include_prosody": include_prosody,
                    "transcription_ms": response_data.get("transcription_ms"),
                    "prosody_ms": response_data.get("prosody_ms"),
                    "total_ms": int((time.perf_counter() - req_start) * 1000),
                },
            )
        except Exception:
            pass

        # Persistência mínima em SQLite
        try:
            session = SessionLocal()
            # Transcrição
            seg_dicts = [
                {"start_s": s.start_s, "end_s": s.end_s, "text": s.text}
                for s in dto.segments
            ]
            tr = db_models.Transcript(
                interaction_id=dto.interaction_id,
                language=dto.language,
                model=dto.model,
                text=dto.text,
                segments=seg_dicts,
            )
            session.merge(tr)

            # Prosódia opcional
            if include_prosody and response_data.get("prosody"):
                pr = response_data["prosody"]
                pf = db_models.ProsodyFeatures(
                    interaction_id=dto.interaction_id,
                    duration_s=pr.get("duration_s"),
                    rms_mean=pr.get("rms_mean"),
                    rms_std=pr.get("rms_std"),
                    zcr_mean=pr.get("zcr_mean"),
                    zcr_std=pr.get("zcr_std"),
                    f0_mean=pr.get("f0_mean"),
                    f0_std=pr.get("f0_std"),
                )
                session.merge(pf)

            session.commit()
        except Exception as db_exc:
            logging.getLogger(__name__).warning("Falha ao persistir no SQLite: %s", db_exc)
            try:
                session.rollback()
            except Exception:
                pass
        finally:
            try:
                session.close()
            except Exception:
                pass

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
