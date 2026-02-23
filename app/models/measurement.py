from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Measurement(Base):
    __tablename__ = "measurements"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensors.id"), nullable=False, index=True)
    created_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    h3_index: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    pm25: Mapped[float] = mapped_column(Float, nullable=False)
    pm10: Mapped[float] = mapped_column(Float, nullable=False)
    no2: Mapped[float] = mapped_column(Float, nullable=False)
    o3: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    sensor = relationship("Sensor", back_populates="measurements")
    created_by = relationship("User")
