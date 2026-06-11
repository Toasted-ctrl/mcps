from dotenv import load_dotenv
import os

from shared.errors import ConfigurationError
from shared.logger import get_logger

log = get_logger()

class MCPConfig:

    REQUIRED_VARS = [
        "PROD_DB_DIALECT",
        "PROD_DB_DRIVER",
        "PROD_DB_PORT",
        "PROD_DB_HOSTNAME",
        "PROD_DB_DATABASE",
        "RS_DB_USER",
        "RS_DB_PASSWORD",
        "RUNESCAPE_GE_ITEM_ID",
        "RUNESCAPE_HISCORE_URL",
        "PROMETHEUS_PORT",
        "MCP_PORT"
    ]

    def __init__(self):

        log.info("Loading configuration")
        log.info("Loading environment variables")
        load_dotenv()

        missing = [var for var in self.REQUIRED_VARS if not os.getenv(var)]
        if missing:
            raise ConfigurationError(f"Missing required environment variables: {', '.join(missing)}")

        self.db_dialect: str = os.getenv("PROD_DB_DIALECT")
        self.db_driver: str = os.getenv("PROD_DB_DRIVER")
        self.db_port: str = os.getenv("PROD_DB_PORT")
        self.db_hostname: str = os.getenv("PROD_DB_HOSTNAME")
        self.db_database: str = os.getenv("PROD_DB_DATABASE")
        self.db_username: str = os.getenv("RS_DB_USER")
        self.db_password: str = os.getenv("RS_DB_PASSWORD")

        self.RS_GE_LINK: str = os.getenv("RUNESCAPE_GE_ITEM_ID")
        self.RS_HS_LINK: str = os.getenv("RUNESCAPE_HISCORE_URL")

        self.NAME: str = os.getenv("MCP_NAME")

        self.PROMETHEUS_PORT: str = int(os.getenv("PROMETHEUS_PORT"))
        self.MCP_PORT: int = int(os.getenv("MCP_PORT"))

        log.info("Loaded configuration")

    @property
    def db_url(self) -> str:
        return (
            f"{self.db_dialect}+{self.db_driver}://"
            f"{self.db_username}:{self.db_password}@"
            f"{self.db_hostname}:{self.db_port}/{self.db_database}"
        )

config = MCPConfig()