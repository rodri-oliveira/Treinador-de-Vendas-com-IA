from src.domain.entities.transcript import TranscriptDTO


def test_transcript_dto_segments_default_factory_independence():
    a = TranscriptDTO(text="a")
    b = TranscriptDTO(text="b")

    # Listas independentes
    assert a.segments == []
    assert b.segments == []

    a.segments.append(
        # Usamos um dict compatível para simular segmento rapidamente
        type("Seg", (), {"start_s": 0.0, "end_s": 1.0, "text": "x"})()
    )

    assert len(a.segments) == 1
    assert b.segments == []

