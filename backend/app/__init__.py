import time
from pathlib import Path

from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import delete, select

from .database import SessionLocal
from .models import Member, Team
from .routes import router, v1_router

TEAM_NAME = "Blbí a Blbější"
TEAM_MEMBERS = ["Adamooss0", "NoeThaKatze"]

BASE_DIR = Path(__file__).resolve().parent.parent


def run_migrations() -> None:
    """Přivede databázi na nejnovější verzi schématu (alembic upgrade head)."""
    cfg = Config(str(BASE_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(BASE_DIR / "alembic"))
    command.upgrade(cfg, "head")


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

    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    app.include_router(router)
    app.include_router(v1_router)

    for attempt in range(30):
        try:
            run_migrations()
            seed_team()
            break
        except Exception as e:
            print(f"DB ještě není připravená ({attempt + 1}/30): {e}", flush=True)
            time.sleep(3)
    else:
        raise RuntimeError("Nepodařilo se připravit databázi")

    return app
