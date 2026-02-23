from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.audit import write_audit_log
from app.core.security import ROLE_ADMIN, ROLE_OPERATOR, require_roles
from app.db.session import get_db
from app.models.measurement import Measurement
from app.models.user import User
from app.schemas.measurement import MeasurementCreate, MeasurementOut
from app.services.event_bus import EventDispatcher
from app.services.measurement_service import create_measurement

router = APIRouter(prefix="/measurements", tags=["measurements"])


@router.post("", response_model=MeasurementOut, status_code=status.HTTP_201_CREATED)
def create_measurement_endpoint(
    payload: MeasurementCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(ROLE_ADMIN, ROLE_OPERATOR)),
) -> Measurement:
    dispatcher: EventDispatcher = request.app.state.dispatcher

    try:
        measurement = create_measurement(db, current_user, payload, dispatcher)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    write_audit_log(
        db,
        user_id=current_user.id,
        action="MEASUREMENT_CREATE",
        resource="measurement",
        details=f"measurement_id={measurement.id};h3={measurement.h3_index}",
    )
    return measurement


@router.get("/by-h3/{h3_index}", response_model=list[MeasurementOut])
def get_measurements_by_h3(
    h3_index: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(ROLE_ADMIN, ROLE_OPERATOR)),
) -> list[Measurement]:
    return (
        db.query(Measurement)
        .filter(Measurement.h3_index == h3_index)
        .order_by(Measurement.created_at.desc())
        .all()
    )
