from datetime import datetime

from pydantic import BaseModel


class AirQualityAggregateOut(BaseModel):
    h3_index: str
    measurement_count: int
    avg_pm25: float
    avg_pm10: float
    avg_no2: float
    avg_o3: float
    updated_at: datetime

    model_config = {"from_attributes": True}
