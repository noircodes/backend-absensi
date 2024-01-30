from enum import Enum
from typing import List, Optional
from bson import ObjectId
from pydantic import Field
from config.mongodb_collections import DB_USER

from models.model_utils import DefaultModel
from utils.datatypes_util import ObjectIdStr, BaseModel

from utils.datetimes_util import DatetimeUtils

class RoleType(str, Enum):
    ADMIN = "ADMIN"
    EMPLOYEE = "EMPLOYEE"
    
class UserUpdate(BaseModel):
    name: str
    photoUrl: str = None
    email: str = None
    phone: str = None
    tags: List[str] = None

class UserRequest(UserUpdate):
    username: str
    password: str
    noId: Optional[str] = None
    role: RoleType = None
    
class UserView(UserRequest, DefaultModel):
    pass

class UserResponse(UserUpdate, DefaultModel):
    username: str
    noId: Optional[str] = None
    role: RoleType = None
    
class UserInDb(UserRequest, DefaultModel):
    id: ObjectIdStr = Field(alias="_id")
    
user_instance = UserView(
    createTime=DatetimeUtils.datetime_now(),
    createdBy=None,
    updateTime=None,
    updatedBy=None,
    isDelete=False,
    deleteBy=None,
    deleteTime=None,
    name="Administrator",
    photoUrl="string",
    email="admin@mail.com",
    phone="08123456789",
    tags=[],
    username="admin",
    password="admin",
    noId="A1",
    role=RoleType.ADMIN
)

async def create_user_instances():
    await DB_USER.insert_one(user_instance.model_dump())