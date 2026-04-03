from pydentic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "PyStore"
    debug: bool = True
    database_url: str = "sqlite:///./shop.db"
    cores_origins: list = [
        "http://localhost:5173",
        "http://localhost:3000"
    ]
    static_dir: str = "static"
    images_dir: str ="static/images"

    class Config:
        env_file = ".env"

settings = Settings()