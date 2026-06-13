from dotenv import load_dotenv
from pathlib import Path

from shared.config import BaseConfig
from shared.logger import get_logger

load_dotenv(Path(__file__).parent / ".env")

class MCPConfig(BaseConfig):

    """MCP Config"""

    def __init__(self):
        super().__init__()
        log = get_logger(self.MCP_NAME)
        log.info(f"Finished setting up config")

config = MCPConfig()