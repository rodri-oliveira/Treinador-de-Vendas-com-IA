import argparse
import os
import sys
from pathlib import Path
from sqlalchemy.orm import joinedload

# Garante que a raiz do projeto esteja no sys.path para imports via 'src.*'
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.infrastructure.db.sqlite import SessionLocal
from src.infrastructure.db import models as db_models


def list_last(limit: int = 5):
    session = SessionLocal()
    try:
        trs = (
            session.query(db_models.Transcript)
            .options(joinedload(db_models.Transcript.prosody))
            .order_by(db_models.Transcript.created_at.desc())
            .limit(limit)
            .all()
        )
        print(f"Last {len(trs)} transcripts:")
        for t in trs:
            has_prosody = "yes" if t.prosody else "no"
            segs = len(t.segments or [])
            print(f"- id={t.interaction_id} lang={t.language} model={t.model} segments={segs} prosody={has_prosody} created_at={t.created_at}")
    finally:
        session.close()


def main():
    parser = argparse.ArgumentParser(description="Inspect SQLite transcripts/prosody")
    parser.add_argument("--limit", type=int, default=5, help="How many records to show")
    args = parser.parse_args()

    # Show which DB in use
    db_url = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")
    print(f"Database: {db_url}")
    list_last(limit=args.limit)


if __name__ == "__main__":
    main()
