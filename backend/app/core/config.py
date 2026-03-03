from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_HOST: str = "localhost"
    MONGODB_PORT: int = 27017
    MONGODB_DB_NAME: str = "bytebrief"

    # Auth
    SECRET_KEY: str = "dev_secret_key_change_me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # External APIs
    NEWSAPI_KEY: Optional[str] = None

    # NLP Model Settings
    SUMMARIZER_MODEL: str = "facebook/bart-large-cnn"
    SUMMARIZER_MAX_LENGTH: int = 300
    SUMMARIZER_MIN_LENGTH: int = 80
    SUMMARIZER_NUM_BEAMS: int = 4

    SIMILARITY_MODEL: str = "all-mpnet-base-v2"
    DUPLICATE_THRESHOLD: float = 0.78

    # Scraper
    SCRAPE_INTERVAL_MINUTES: int = 30
    SCRAPER_USER_AGENT: str = "ByteBriefBot/1.0"

    # Whoosh Index
    WHOOSH_INDEX_DIR: str = "./data/whoosh_index"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
