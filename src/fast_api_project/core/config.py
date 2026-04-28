# Configuration settings
import os
from typing import Optional

class Settings:
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:123456@localhost:3306/fastapi")

    # Application settings
    APP_TITLE: str = "OH~MY~~API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

settings = Settings()