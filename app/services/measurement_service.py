from sqlalchemy.orm import Session

from app.models.measurement import Measurement
from app.models.sensor import Sensor
from app.models.user import User
from app.schemas.measurement import MeasurementCreate
from app.services.event_bus import EventDispatcher
from app.utils.h3_utils import latlon_to_h3


def create_measurement(
    db: Session,
    current_user: User,
    payload: MeasurementCreate,
    dispatcher: EventDispatcher,
) -> Measurement:
    sensor = db.query(Sensor).filter(Sensor.id == payload.sensor_id).first()
    if not sensor:
        raise ValueError("Sensor not found")

    h3_index = latlon_to_h3(payload.latitude, payload.longitude)

    measurement = Measurement(
        sensor_id=payload.sensor_id,
        created_by_user_id=current_user.id,
        latitude=payload.latitude,
        longitude=payload.longitude,
        h3_index=h3_index,
        pm25=payload.pm25,
        pm10=payload.pm10,
        no2=payload.no2,
        o3=payload.o3,
    )

    db.add(measurement)
    db.commit()
    db.refresh(measurement)

    dispatcher.publish(
        "measurement.created",
        {
            "measurement_id": measurement.id,
            "h3_index": measurement.h3_index,
        },
    )
    return measurement
