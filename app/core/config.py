from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    PROJECT_NAME: str = "Mini Social Network"
    PROJECT_DESCRIPTION :str = "Mini Social Network API - Intervyu uchun tayyorlangan loyiha"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432

    SECRET_KEY: str
    ALGORITHMS: list[str] = ['HS256']
    ACCESS_TOKEN_EXPIRE_MINUTES:  int= 1440

    DATABASE_URL: str | None = None

    @property
    def get_database_url(self):
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # 3. Pydantic'ga faylning mutlaq manzilini beramiz
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        extra="ignore",
        env_file_encoding="utf-8"
    )
settings = Settings()
