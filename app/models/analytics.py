from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AirQualityAggregate(Base):
    __tablename__ = "air_quality_aggregates"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    h3_index: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    measurement_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    avg_pm25: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    avg_pm10: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    avg_no2: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    avg_o3: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
