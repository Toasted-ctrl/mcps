from dotenv import load_dotenv
from pathlib import Path

from shared.config import BaseConfig

load_dotenv(Path(__file__).parent / ".env")

class MCPConfig(BaseConfig):

    def __init__(self):
        super().__init__()

config = MCPConfig()