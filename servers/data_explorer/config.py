from pathlib import Path
import os

from shared.config import BaseConfig

class MCPConfig(BaseConfig):

    ADDITIONAL_VARS = [
        "DB_DATABASES",
        "DB_PASSWORD",
        "DB_HOSTNAME",
        "DB_USERNAME",
        "DB_DIALECT",
        "DB_DRIVER",
        "DB_PORT",
    ]

    REQUIRED_VARS = BaseConfig.REQUIRED_VARS + ADDITIONAL_VARS

    def __init__(self):
        super().__init__(env_path=Path(__file__).parent / ".env")
        self.DB_DATABASES: list = os.getenv("DB_DATABASES").split(sep=",")
        self.DB_PASSWORD: str = os.getenv("DB_PASSWORD")
        self.DB_HOSTNAME: str = os.getenv("DB_HOSTNAME")
        self.DB_USERNAME: str = os.getenv("DB_USERNAME")
        self.DB_DIALECT: str = os.getenv("DB_DIALECT")
        self.DB_DRIVER: str = os.getenv("DB_DRIVER")
        self.DB_PORT: int = int(os.getenv("DB_PORT"))


    def db_url(self, db_database: str) -> str:
        
        """Creates database url for the database that needs to be accessed."""

        return (
            f"{self.DB_DIALECT}+{self.DB_DRIVER}://"
            f"{self.DB_USERNAME}:{self.DB_PASSWORD}@"
            f"{self.DB_HOSTNAME}:{self.DB_PORT}/{db_database}"
        )

config = MCPConfig()