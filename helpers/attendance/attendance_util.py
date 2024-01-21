from fastapi import HTTPException
from config.mongodb_collections import DB_ATTENDANCE
from models.attendance.model_attendance import AttendanceInDb
from utils.validation_util import ValidationUtils


class AttendanceUtils:
    
    @staticmethod
    async def get_attendance_by_id_or_404(attendance_id: str):
        user = await DB_ATTENDANCE.find_one(
            {"isDelete": False, "_id": ValidationUtils.validate_objectid(attendance_id, "Attendance ID")}
        )
        if not user:
            raise HTTPException(status_code=404, detail="User tidak ditemukan")
        return AttendanceInDb(**user)

    @staticmethod
    async def get_attendance_by_id(attendance_id: str):
        user = await DB_ATTENDANCE.find_one(
            {"isDelete": False, "_id": ValidationUtils.validate_objectid(attendance_id, "Attendance ID")}
        )
        if not user:
            return False
        return AttendanceInDb(**user)