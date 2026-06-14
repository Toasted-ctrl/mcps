from dotenv import load_dotenv
from pathlib import Path
import os

from shared.config import BaseConfig

load_dotenv(Path(__file__).parent / ".env")

class MCPConfig(BaseConfig):

    ADDITIONAL_VARS = [
        "PROD_DB_DIALECT",
        "PROD_DB_DRIVER",
        "PROD_DB_PORT",
        "PROD_DB_HOSTNAME",
        "PROD_DB_DATABASE",
        "RS_DB_USER",
        "RS_DB_PASSWORD",
        "RUNESCAPE_GE_ITEM_ID",
        "RUNESCAPE_HISCORE_URL"
    ]

    REQUIRED_VARS = BaseConfig.REQUIRED_VARS + ADDITIONAL_VARS

    def __init__(self):
        super().__init__()

        self.DB_DIALECT: str = os.getenv("PROD_DB_DIALECT")
        self.DB_DRIVER: str = os.getenv("PROD_DB_DRIVER")
        self.DB_PORT: str = os.getenv("PROD_DB_PORT")
        self.DB_HOSTNAME: str = os.getenv("PROD_DB_HOSTNAME")
        self.DB_DATABASE: str = os.getenv("PROD_DB_DATABASE")
        self.DB_USERNAME: str = os.getenv("RS_DB_USER")
        self.DB_PASSWORD: str = os.getenv("RS_DB_PASSWORD")

        self.RS_GE_LINK: str = os.getenv("RUNESCAPE_GE_ITEM_ID")
        self.RS_HS_LINK: str = os.getenv("RUNESCAPE_HISCORE_URL")

    @property
    def DB_URL(self) -> str:
        return (
            f"{self.DB_DIALECT}+{self.DB_DRIVER}://"
            f"{self.DB_USERNAME}:{self.DB_PASSWORD}@"
            f"{self.DB_HOSTNAME}:{self.DB_PORT}/{self.DB_DATABASE}"
        )

config = MCPConfig()