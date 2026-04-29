from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://user:password@localhost:5432/orders_db"
    rabbitmq_host: str = "localhost"
    
    # Pydantic automaticky zkusí načíst hodnoty z environmentálních proměnných
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
