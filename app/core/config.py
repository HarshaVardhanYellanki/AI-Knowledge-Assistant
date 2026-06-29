import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    CHAT_MODEL = os.getenv("CHAT_MODEL")

    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

    QDRANT_URL = os.getenv("QDRANT_URL")

    QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")

    MONGODB_URI = os.getenv("MONGODB_URI")

    DATABASE_NAME = os.getenv("DATABASE_NAME")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
    )


settings = Settings()