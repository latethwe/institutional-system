from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.security import ROLE_ADMIN, require_roles
from app.db.session import get_db
from app.models.audit_log import AuditLog
from app.models.user import User

router = APIRouter(prefix="/audit-logs", tags=["audit"])


class AuditLogOut(BaseModel):
    id: int
    user_id: int | None
    action: str
    resource: str
    details: str
    created_at: datetime

    model_config = {"from_attributes": True}


@router.get("", response_model=list[AuditLogOut])
def list_audit_logs(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(ROLE_ADMIN)),
) -> list[AuditLog]:
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).all()
