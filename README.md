# Tour-de-App

Projekt skupiny Blbej a Blbější.

## Database

The schema is managed with Alembic migrations (`backend/alembic/`) and applied
automatically on server start (`alembic upgrade head`, called from
`backend/app/__init__.py`), so a fresh empty database needs no manual setup.

To change the schema, edit the models in `backend/app/models.py` and run
`alembic revision --autogenerate -m "description"` in the `backend` directory.
