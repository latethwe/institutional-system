from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Institutional Environmental Monitoring System")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./institutional.db")
    h3_resolution: int = int(os.getenv("H3_RESOLUTION", "9"))
    secret_key: str = os.getenv("SECRET_KEY", "institutional-demo-secret")


settings = Settings()
