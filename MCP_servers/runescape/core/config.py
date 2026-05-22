import os

from dotenv import load_dotenv

class MCPConfig:
    load_dotenv()

    db_dialect = os.getenv("PROD_DB_DIALECT")
    db_driver = os.getenv("PROD_DB_DRIVER")
    db_port = os.getenv("PROD_DB_PORT")
    db_hostname = os.getenv("PROD_DB_HOSTNAME")
    db_database = os.getenv("PROD_DB_DATABASE")
    db_username = os.getenv("RS_DB_USER")
    db_password = os.getenv("RS_DB_PASSWORD")

    @property
    def db_url(self) -> str:
        return f"{self.db_dialect}+{self.db_driver}://{self.db_username}:{self.db_password}@{self.db_hostname}:{self.db_port}/{self.db_database}"

mcp_config = MCPConfig()