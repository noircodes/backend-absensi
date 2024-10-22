from typing import Any
import yaml
from motor.motor_asyncio import AsyncIOMotorClient
from config.mongodb_type_checking import TMongoClient, TMongoDatabase

# CONFIG USING YAML
def load_config() -> dict[str, Any]:
    with open("config/setting.yml") as yaml_file:
        conf = yaml.load(yaml_file.read(), Loader=yaml.SafeLoader)
    return conf

CONF = load_config()

DEBUG = CONF.get("project", dict())["debug"]
JWT_SECRET_KEY: str = CONF.get("project", dict())["key"]
PROJECT_NAME = CONF.get("project", dict())["projectName"]
JWT_ALGORITHM: str = CONF.get("project", dict())["algorithm"]
ACCESS_TOKEN_EXPIRE_MINUTES = CONF.get("project", dict())["tokenExpiredInMinutes"]
ENVIRONMENT = CONF.get("project", dict())["environment"]

MGDB_CLIENT: TMongoClient = AsyncIOMotorClient(
    host=CONF.get("mongodb", dict())["HOST"],
    port=CONF.get("mongodb", dict())["PORT"]
)

DB_ABSENSI: TMongoDatabase = MGDB_CLIENT[CONF.get("mongodb", dict())["NAME"]]

# CONFIG USING ENV

# Load environment variables from .env file
# load_dotenv()

# DEBUG = os.getenv("DEBUG")
# JWT_SECRET_KEY = os.getenv("KEY")
# PROJECT_NAME = os.getenv("PROJECT_NAME")
# JWT_ALGORITHM = os.getenv("ALGORITHM")
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRED_IN_MINUTES"))

# MGDB_CLIENT = AsyncIOMotorClient(os.getenv("MONGO_URL"))

# DB_ABSENSI = MGDB_CLIENT[os.getenv("NAME")]