import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routes import health_router, router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Python FastAPI Backend Template",
        description="API for students to start coding. Simple list of product at school buffet.",
    )

    # Allow a frontend dev server on another port (e.g. localhost:3001) to call the API.
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    app.include_router(health_router)
    app.include_router(router)

    for attempt in range(30):
        try:
            Base.metadata.create_all(bind=engine)
            break
        except Exception as e:
            print(f"DB ještě není připravená ({attempt + 1}/30): {e}", flush=True)
            time.sleep(3)
    else:
        raise RuntimeError("Nepodařilo se vytvořit tabulky")

    return app
