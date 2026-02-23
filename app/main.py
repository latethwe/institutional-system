from fastapi import FastAPI

from app.api.analytics import router as analytics_router
from app.api.audit import router as audit_router
from app.api.auth import router as auth_router
from app.api.measurements import router as measurements_router
from app.core.config import settings
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.services.analytics_service import update_aggregate_for_h3
from app.services.event_bus import EventDispatcher

app = FastAPI(title=settings.app_name, version="1.0.0")


def register_event_handlers(dispatcher: EventDispatcher) -> None:
    def on_measurement_created(payload: dict) -> None:
        db = SessionLocal()
        try:
            h3_index = payload.get("h3_index")
            if h3_index:
                update_aggregate_for_h3(db, h3_index)
        finally:
            db.close()

    dispatcher.subscribe("measurement.created", on_measurement_created)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    dispatcher = EventDispatcher()
    register_event_handlers(dispatcher)
    app.state.dispatcher = dispatcher


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(measurements_router)
app.include_router(analytics_router)
app.include_router(audit_router)
