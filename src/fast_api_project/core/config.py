# Configuration settings
import logging
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class DatabaseSettings:
    """Database connection settings (data container)"""

    def __init__(self, URL: str = "mysql+pymysql://root:123456@localhost:3306/fastapi"):
        self.URL = URL


class AppSettings:
    """Application metadata settings (data container)"""

    def __init__(self, TITLE: str = "OH~MY~~API", VERSION: str = "1.0.0", DEBUG: bool = False):
        self.TITLE = TITLE
        self.VERSION = VERSION
        self.DEBUG = DEBUG


class ServerSettings:
    """Server runtime settings (data container)"""

    def __init__(self, HOST: str = "0.0.0.0", PORT: int = 8000):
        self.HOST = HOST
        self.PORT = PORT


class SecuritySettings:
    """Security & JWT settings (data container)"""

    def __init__(self, SECRET_KEY: Optional[str] = None, ALGORITHM: str = "HS256", ACCESS_TOKEN_EXPIRE_MINUTES: int = 30):
        self.SECRET_KEY = SECRET_KEY
        self.ALGORITHM = ALGORITHM
        self.ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env file.

    Environment variables set in the OS shell take precedence over those in .env.
    Access settings via grouped properties: settings.database.URL, settings.app.TITLE, etc.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Database (prefix: DATABASE_) ---
    DATABASE_URL: str = "mysql+pymysql://root:123456@localhost:3306/fastapi"

    # --- Application (prefix: APP_) ---
    APP_TITLE: str = "OH~MY~~API"
    APP_VERSION: str = "1.0.0"
    APP_DEBUG: bool = False

    # --- Server (prefix: SERVER_) ---
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000

    # --- Security (prefix: SECURITY_) ---
    SECURITY_SECRET_KEY: Optional[str] = None
    SECURITY_ALGORITHM: str = "HS256"
    SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def database(self) -> DatabaseSettings:
        """Nested access: settings.database.URL"""
        return DatabaseSettings(URL=self.DATABASE_URL)

    @property
    def app(self) -> AppSettings:
        """Nested access: settings.app.TITLE, settings.app.VERSION, settings.app.DEBUG"""
        return AppSettings(
            TITLE=self.APP_TITLE,
            VERSION=self.APP_VERSION,
            DEBUG=self.APP_DEBUG,
        )

    @property
    def server(self) -> ServerSettings:
        """Nested access: settings.server.HOST, settings.server.PORT"""
        return ServerSettings(
            HOST=self.SERVER_HOST,
            PORT=self.SERVER_PORT,
        )

    @property
    def security(self) -> SecuritySettings:
        """Nested access: settings.security.*"""
        return SecuritySettings(
            SECRET_KEY=self.SECURITY_SECRET_KEY,
            ALGORITHM=self.SECURITY_ALGORITHM,
            ACCESS_TOKEN_EXPIRE_MINUTES=self.SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES,
        )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.SECURITY_SECRET_KEY is None:
            logger.warning(
                "SECURITY_SECRET_KEY is not set. "
                "Please set it in production environment."
            )


settings = Settings()