
from decouple import config


class Settings:
    DATABASE_HOSTNAME = config('DATABASE_HOSTNAME')
    DATABASE_PORT = config('DATABASE_PORT')
    DATABASE_PASSWORD = config('DATABASE_PASSWORD')
    DATABASE_NAME = config('DATABASE_NAME')
    DATABASE_USERNAME = config('DATABASE_USERNAME')
    SECRET_KEY = config('SECRET_KEY')
    ALGORITHM = config('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES')


settings = Settings()
