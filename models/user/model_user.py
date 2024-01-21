from enum import Enum
from typing import List, Optional
from bson import ObjectId
from pydantic import Field

from models.model_utils import DefaultModel
from utils.datatypes_util import ObjectIdStr, BaseModel

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
    
class UserInDb(UserRequest, DefaultModel):
    id: ObjectIdStr = Field(alias="_id")