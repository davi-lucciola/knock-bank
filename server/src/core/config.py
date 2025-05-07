import os
import dotenv as env
from pydantic_settings import BaseSettings


env.load_dotenv()


class Settings(BaseSettings):
    API_TITLE: str = 'Knock Bank API'
    DOCS_URL: str = '/api/docs'
    DESCRIPTION: str = 'API para gerenciar transacoes bancarias do Knock Bank'

    SHOW_SQL: bool = os.getenv('SHOW_SQL', False)
    DATABASE_URI: str = os.getenv('SQLALCHEMY_DATABASE_URI')

    # JWT
    ALGORITHM: str = 'HS256'
    TOKEN_SECRET: str = os.getenv('TOKEN_SECRET')
    EXPIRATION_SECONDS: int = 60 * 60 * 5  # 5 Hours


settings = Settings()
