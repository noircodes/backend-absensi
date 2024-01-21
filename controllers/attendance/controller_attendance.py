from datetime import time, timedelta
from typing import List

from fastapi import HTTPException

from helpers.attendance.helper_attendance import AttendanceHelper
from models.attendance.model_attendance import Attendance, AttendanceInDb, Checks, StatusType
from utils.datatypes_util import ObjectIdStr
from utils.datetimes_util import DatetimeUtils
from utils.validation_util import ValidationUtils


class AttendanceController:
    
    @staticmethod
    async def get_all_attendances() -> List[AttendanceInDb]:
        return await AttendanceHelper.get_all_attendances()
    
    @staticmethod
    async def get_attendance_by_id(
        id: ObjectIdStr
    ) -> AttendanceInDb:
        return await AttendanceHelper.get_attendance_by_id(id)
    
    @staticmethod
    async def tap_attendance(
        attendance_method: str,
        user_id: ObjectIdStr
    ) -> AttendanceInDb:
        if user_id:
            user_id = ValidationUtils.validate_objectid(user_id, "UserId")
        timestamp = DatetimeUtils.datetime_now()
        check_today_attendance = await AttendanceHelper.get_attendance_by_employee_id_and_today(
            user_id
        )
        if not check_today_attendance:
            if DatetimeUtils.time_now() > time(hour=8):
                status = StatusType.ON_TIME
            else:
                status = StatusType.NOT_ON_TIME
            request = Attendance(
                checkIn=Checks(
                    timestamp=timestamp,
                    status=status,
                    attendanceMethod=attendance_method
                )
            )
            return await AttendanceHelper.create_attendance(request, user_id)
        else:
            if check_today_attendance.checkIn.timestamp + timedelta(minutes=30) >= DatetimeUtils.datetime_now():
                raise HTTPException(400, "Anda sudah melakukan Check In hari ini.")
            if DatetimeUtils.time_now() > time(hour=17):
                status = StatusType.ON_TIME
            else:
                status = StatusType.NOT_ON_TIME
            request = Attendance(
                checkOut=Checks(
                    timestamp=timestamp,
                    status=status,
                    attendanceMethod=attendance_method
                )
            )
            is_already_check_out = await AttendanceHelper.get_attendance_by_employee_id_and_today(user_id, True)
            if is_already_check_out:
                raise HTTPException(400, "Anda sudah melakukan Check Out hari ini.")
            return await AttendanceHelper.update_attendance(check_today_attendance.id, request, user_id)
        
    @staticmethod
    async def delete_attendance(
        id: ObjectIdStr,
        user_id: ObjectIdStr
    ) -> AttendanceInDb:
        current_data = await AttendanceHelper.get_attendance_by_id(id)
        
        return await AttendanceHelper.delete_attendance(id, user_id)