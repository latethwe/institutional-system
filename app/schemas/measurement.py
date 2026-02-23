from datetime import datetime

from pydantic import BaseModel, Field


class MeasurementCreate(BaseModel):
    sensor_id: int
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    pm25: float = Field(ge=0)
    pm10: float = Field(ge=0)
    no2: float = Field(default=0, ge=0)
    o3: float = Field(default=0, ge=0)


class MeasurementOut(BaseModel):
    id: int
    sensor_id: int
    created_by_user_id: int
    latitude: float
    longitude: float
    h3_index: str
    pm25: float
    pm10: float
    no2: float
    o3: float
    created_at: datetime

    model_config = {"from_attributes": True}
