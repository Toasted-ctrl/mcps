from dotenv import load_dotenv
import os
import sys

from shared.logger import get_logger

class MCPConfig:

    REQUIRED_VARS = [
        "MCP_NAME",
        "MCP_PORT",
        "PROMETHEUS_PORT"
    ]

    def __init__(self):
        load_dotenv()
        missing = [var for var in self.REQUIRED_VARS if not os.getenv(var)]
        if missing:
            sys.exit(f"Missing environment variables {', '.join(missing)}")

        log = get_logger(name=os.getenv("MCP_NAME"))
        log.info("Setting up config")

        self.PROMETHEUS_PORT: int = int(os.getenv("PROMETHEUS_PORT"))
        self.MCP_PORT: int = int(os.getenv("MCP_PORT"))
        self.MCP_NAME: str = os.getenv("MCP_NAME")

        log.info("Finished setting up config")

config = MCPConfig()