from dotenv import load_dotenv
import os

from logger.logger import get_logger

log = get_logger()

class MCP_Config:
    log.info("Loading environment variables")
    load_dotenv()
    PROMETHEUS_PORT: int = int(os.getenv("PROMETHEUS_PORT"))
    MCP_PORT: int = int(os.getenv("MCP_PORT"))

config = MCP_Config()