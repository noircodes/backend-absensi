import os
from dotenv import load_dotenv
import yaml
from motor.motor_asyncio import AsyncIOMotorClient

# CONFIG USING YAML
# def load_config() -> dict:
#     with open("config/setting.yml") as yaml_file:
#         conf = yaml.load(yaml_file.read(), Loader=yaml.SafeLoader)
#     return conf


# CONF = load_config()

# DEBUG = CONF.get("project", dict())["debug"]
# JWT_SECRET_KEY = CONF.get("project", dict())["key"]
# PROJECT_NAME = CONF.get("project", dict())["projectName"]
# JWT_ALGORITHM = CONF.get("project", dict())["algorithm"]
# ACCESS_TOKEN_EXPIRE_MINUTES = CONF.get("project", dict())["tokenExpiredInMinutes"]

# MGDB_CLIENT = AsyncIOMotorClient(
#     host=CONF.get("mongodb", dict())["HOST"],
#     port=CONF.get("mongodb", dict())["PORT"]
# )

# DB_ABSENSI = MGDB_CLIENT[CONF.get("mongodb", dict())["NAME"]]

# CONFIG USING ENV

# Load environment variables from .env file
load_dotenv()

DEBUG = os.getenv("DEBUG")
JWT_SECRET_KEY = os.getenv("KEY")
PROJECT_NAME = os.getenv("PROJECT_NAME")
JWT_ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRED_IN_MINUTES"))

MGDB_CLIENT = AsyncIOMotorClient(os.getenv("MONGO_URL"))

DB_ABSENSI = MGDB_CLIENT[os.getenv("NAME")]