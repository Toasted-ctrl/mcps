import os
import sys

from .logger import get_logger

class BaseConfig:

    """Base configuration class which import the minimum environment variables required to run the MCP.
    To add additional required variables, just use BaseConfig.REQUIRED_VARS + []"""

    REQUIRED_VARS = [
        "PROMETHEUS_PORT",
        "MCP_NAME",
        "MCP_PORT"
    ]

    def __init__(self):
        missing = [var for var in self.REQUIRED_VARS if not os.getenv(var)]
        if missing:
            sys.exit(f"Missing environment variables: {', '.join(missing)}")
        log = get_logger(os.getenv("MCP_NAME"))
        log.info(f"Setting up config for {os.getenv("MCP_NAME")}")

        self.MCP_NAME: str = os.getenv("MCP_NAME")
        self.MCP_PORT: int = int(os.getenv("MCP_PORT"))
        self.PROMETHEUS_PORT: int = int(os.getenv("PROMETHEUS_PORT"))