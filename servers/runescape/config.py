from dotenv import load_dotenv
import os
import sys

from shared.logger import get_logger

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
        "MCP_PORT",
        "MCP_NAME"
    ]

    def __init__(self):
        load_dotenv()
        missing = [var for var in self.REQUIRED_VARS if not os.getenv(var)]
        if missing:
            sys.exit(f"Missing environment variables: {', '.join(missing)}")

        log = get_logger(name=os.getenv("MCP_NAME"))
        log.info("Setting up config")

        self.DB_DIALECT: str = os.getenv("PROD_DB_DIALECT")
        self.DB_DRIVER: str = os.getenv("PROD_DB_DRIVER")
        self.DB_PORT: str = os.getenv("PROD_DB_PORT")
        self.DB_HOSTNAME: str = os.getenv("PROD_DB_HOSTNAME")
        self.DB_DATABASE: str = os.getenv("PROD_DB_DATABASE")
        self.DB_USERNAME: str = os.getenv("RS_DB_USER")
        self.DB_PASSWORD: str = os.getenv("RS_DB_PASSWORD")

        self.RS_GE_LINK: str = os.getenv("RUNESCAPE_GE_ITEM_ID")
        self.RS_HS_LINK: str = os.getenv("RUNESCAPE_HISCORE_URL")

        self.MCP_NAME: str = os.getenv("MCP_NAME")

        self.PROMETHEUS_PORT: str = int(os.getenv("PROMETHEUS_PORT"))
        self.MCP_PORT: int = int(os.getenv("MCP_PORT"))

        log.info("Finished setting up config")

    @property
    def DB_URL(self) -> str:
        return (
            f"{self.DB_DIALECT}+{self.DB_DRIVER}://"
            f"{self.DB_USERNAME}:{self.DB_PASSWORD}@"
            f"{self.DB_HOSTNAME}:{self.DB_PORT}/{self.DB_DATABASE}"
        )

config = MCPConfig()