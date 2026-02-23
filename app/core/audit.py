from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def write_audit_log(db: Session, action: str, resource: str, user_id: int | None = None, details: str = "") -> AuditLog:
    entry = AuditLog(user_id=user_id, action=action, resource=resource, details=details)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
