from datetime import datetime
from typing import Optional

from utils.datatypes_util import ObjectIdStr, BaseModel


class DefaultModel(BaseModel):
    createTime: Optional[datetime] = None
    createdBy: Optional[ObjectIdStr] = None
    updateTime: Optional[datetime] = None
    updatedBy: Optional[ObjectIdStr] = None
    isDelete: bool = False
    deleteBy: Optional[ObjectIdStr] = None
    deleteTime: Optional[datetime] = None