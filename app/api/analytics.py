from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import ROLE_ADMIN, ROLE_ANALYST, ROLE_OPERATOR, enforce_analytics_abac, require_roles
from app.db.session import get_db
from app.models.analytics import AirQualityAggregate
from app.models.user import User
from app.schemas.analytics import AirQualityAggregateOut

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/region/{h3_index}", response_model=AirQualityAggregateOut)
def get_region_analytics(
    h3_index: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(ROLE_ADMIN, ROLE_OPERATOR, ROLE_ANALYST)),
) -> AirQualityAggregate:
    enforce_analytics_abac(current_user, h3_index)

    aggregate = db.query(AirQualityAggregate).filter(AirQualityAggregate.h3_index == h3_index).first()
    if not aggregate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No analytics for this H3 region")
    return aggregate
