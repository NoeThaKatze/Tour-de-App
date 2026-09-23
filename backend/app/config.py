import os
from urllib.parse import quote_plus


class Settings:
    db_host: str = os.getenv("FASTAPI_DB_HOST", "localhost")
    db_port: int = int(os.getenv("FASTAPI_DB_PORT", "3306"))
    db_name: str = os.getenv("FASTAPI_DB_NAME", "product")
    db_user: str = os.getenv("FASTAPI_DB_USER", "root")
    db_password: str = os.getenv("FASTAPI_DB_PASSWORD", "")

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.db_user}:{quote_plus(self.db_password)}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
