from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.analytics import AirQualityAggregate
from app.models.measurement import Measurement


def update_aggregate_for_h3(db: Session, h3_index: str) -> AirQualityAggregate:
    stats = (
        db.query(
            func.count(Measurement.id),
            func.avg(Measurement.pm25),
            func.avg(Measurement.pm10),
            func.avg(Measurement.no2),
            func.avg(Measurement.o3),
        )
        .filter(Measurement.h3_index == h3_index)
        .one()
    )

    count = int(stats[0] or 0)
    aggregate = db.query(AirQualityAggregate).filter(AirQualityAggregate.h3_index == h3_index).first()
    if not aggregate:
        aggregate = AirQualityAggregate(h3_index=h3_index)
        db.add(aggregate)

    aggregate.measurement_count = count
    aggregate.avg_pm25 = float(stats[1] or 0.0)
    aggregate.avg_pm10 = float(stats[2] or 0.0)
    aggregate.avg_no2 = float(stats[3] or 0.0)
    aggregate.avg_o3 = float(stats[4] or 0.0)
    aggregate.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(aggregate)
    return aggregate
