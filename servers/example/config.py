from dotenv import load_dotenv
import os

from shared.logger import get_logger

log = get_logger()

class MCPConfig:
    log.info("Loading environment variables")
    load_dotenv()
    PROMETHEUS_PORT: int = int(os.getenv("PROMETHEUS_PORT"))
    MCP_PORT: int = int(os.getenv("MCP_PORT"))
    MCP_NAME: str = os.getenv("MCP_NAME")

config = MCPConfig()