from pydantic import BaseSettings


class EnvironmentVariable(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTE: int

    CIPHER_KEY: str

    REDIS_HOSTNAME: str
    REDIS_DATABASE: str
    REDIS_PORT: str
    REDIS_KEY_EXPIRE_MINUTE: int


    class Config:
        env_file = ".env"

environment_variable = EnvironmentVariable()