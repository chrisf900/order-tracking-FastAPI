from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GRPC_PORT: int = 50054
    CATALOG_SERVICE_HOST: str = "catalog_service"
    CATALOG_SERVICE_PORT: int = 50051

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def catalog_service_url(self) -> str:
        return f"{self.CATALOG_SERVICE_HOST}:{self.CATALOG_SERVICE_PORT}"


settings = Settings()
