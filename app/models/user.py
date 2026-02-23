from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    assigned_h3_regions: Mapped[str] = mapped_column(Text, default="", nullable=False)

    role = relationship("Role", back_populates="users")
    sensors = relationship("Sensor", back_populates="owner")
    audit_logs = relationship("AuditLog", back_populates="user")

    def assigned_regions(self) -> set[str]:
        return {region.strip() for region in self.assigned_h3_regions.split(",") if region.strip()}
