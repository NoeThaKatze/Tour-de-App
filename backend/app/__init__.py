import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import delete, select

from .database import Base, SessionLocal, engine
from .models import Member, Team
from .routes import router, v1_router

TEAM_NAME = "Blbí a Blbější"
TEAM_MEMBERS = ["Adamooss0", "NoeThaKatze"]


def seed_team() -> None:
    """Uloží název týmu a členy do databáze (při každém startu je srovná s kódem)."""
    with SessionLocal() as db:
        team = db.scalars(select(Team)).first()
        if team is None:
            team = Team(name=TEAM_NAME)
            db.add(team)
            db.flush()
        else:
            team.name = TEAM_NAME

        db.execute(delete(Member).where(Member.team_id == team.id))
        db.add_all(Member(team_id=team.id, name=n) for n in TEAM_MEMBERS)
        db.commit()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Python FastAPI Backend Template",
        description="API for students to start coding. Simple list of product at school buffet.",
    )

    # Allow a frontend dev server on another port (e.g. localhost:3001) to call the API.
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    app.include_router(v1_router)
    app.include_router(router)

    for attempt in range(30):
        try:
            Base.metadata.create_all(bind=engine)
            seed_team()
            break
        except Exception as e:
            print(f"DB ještě není připravená ({attempt + 1}/30): {e}", flush=True)
            time.sleep(3)
    else:
        raise RuntimeError("Nepodařilo se vytvořit tabulky")

    return app
