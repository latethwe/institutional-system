from sqlalchemy.orm import Session

from app.core.security import ROLE_ADMIN, ROLE_ANALYST, ROLE_OPERATOR, hash_password
from app.db.base import Base
from app.db.session import engine
from app.models.analytics import AirQualityAggregate
from app.models.audit_log import AuditLog
from app.models.measurement import Measurement
from app.models.role import Role
from app.models.sensor import Sensor
from app.models.user import User
from app.utils.h3_utils import latlon_to_h3


def seed_reference_data(db: Session) -> None:
    demo_allowed_h3 = latlon_to_h3(43.2389, 76.8897)
    role_names = [ROLE_ADMIN, ROLE_OPERATOR, ROLE_ANALYST]
    existing_roles = {role.name for role in db.query(Role).all()}

    for role_name in role_names:
        if role_name not in existing_roles:
            db.add(Role(name=role_name))
    db.commit()

    roles_by_name = {role.name: role for role in db.query(Role).all()}

    default_users = [
        {"username": "admin", "password": "admin123", "role": ROLE_ADMIN, "regions": ""},
        {"username": "operator", "password": "operator123", "role": ROLE_OPERATOR, "regions": ""},
        {
            "username": "analyst",
            "password": "analyst123",
            "role": ROLE_ANALYST,
            "regions": demo_allowed_h3,
        },
    ]

    for user_data in default_users:
        user = db.query(User).filter(User.username == user_data["username"]).first()
        if user:
            if user_data["role"] == ROLE_ANALYST:
                user.assigned_h3_regions = user_data["regions"]
                db.add(user)
            continue
        db.add(
            User(
                username=user_data["username"],
                password_hash=hash_password(user_data["password"]),
                role_id=roles_by_name[user_data["role"]].id,
                assigned_h3_regions=user_data["regions"],
            )
        )
    db.commit()

    if not db.query(Sensor).first():
        admin = db.query(User).filter(User.username == "admin").first()
        db.add(Sensor(code="SENSOR-001", description="Default institutional station", owner_id=admin.id if admin else None))
        db.commit()


def init_db() -> None:
    # Explicit imports keep model metadata complete before create_all.
    _ = (Role, User, Sensor, Measurement, AirQualityAggregate, AuditLog)
    Base.metadata.create_all(bind=engine)

    db = Session(bind=engine)
    try:
        seed_reference_data(db)
    finally:
        db.close()
