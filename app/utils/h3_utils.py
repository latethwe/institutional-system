from app.core.config import settings

try:
    import h3
except Exception as exc:
    raise RuntimeError("h3 package is required. Install dependencies from requirements.txt") from exc


def latlon_to_h3(latitude: float, longitude: float, resolution: int = settings.h3_resolution) -> str:
    if hasattr(h3, "latlng_to_cell"):
        return h3.latlng_to_cell(latitude, longitude, resolution)
    return h3.geo_to_h3(latitude, longitude, resolution)
