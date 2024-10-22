from datetime import datetime
from enum import Enum

from pydantic import Field
from models.model_utils import DefaultModel

from utils.datatypes_util import BaseModel, ObjectIdStr


class StatusType(str, Enum):
    ON_TIME = "TEPAT WAKTU"
    NOT_ON_TIME = "TIDAK TEPAT WAKTU"
    
class EmployeeDetail(BaseModel):
    name: str | None = None
    noId: str | None = None
    employeeId: ObjectIdStr | None = None
    photoUrl: str | None = None
    
class Checks(BaseModel):
    timestamp: datetime | None = None
    status: StatusType | None = None
    attendanceMethod: str | None = None

class Attendance(BaseModel):
    checkIn: Checks = Field(default_factory=Checks)
    checkOut: Checks = Field(default_factory=Checks)
    
class AttendanceView(Attendance, DefaultModel):
    employeeDetail: EmployeeDetail = Field(default_factory=EmployeeDetail)
    
class AttendanceInDb(AttendanceView):
    id: ObjectIdStr = Field(alias="_id")