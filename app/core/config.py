from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Leidos Real-Time Eval Suite"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    tcp_host: str = "0.0.0.0"
    tcp_port: int = 9101
    udp_host: str = "0.0.0.0"
    udp_port: int = 9102
    event_buffer_size: int = 200

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
