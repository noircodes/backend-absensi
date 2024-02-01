from datetime import datetime, time, timedelta
import re
from typing import List

from fastapi import HTTPException
from loguru import logger
from config.mongodb_collections import DB_ATTENDANCE

from helpers.attendance.helper_attendance import AttendanceHelper
from models.attendance.model_attendance import Attendance, AttendanceInDb, Checks, StatusType
from utils.datatypes_util import ObjectIdStr
from utils.datetimes_util import DatetimeUtils
from utils.pagination.model_pagination_util import MsPagination, MsPaginationResult
from utils.pagination.pagination_util import Paginate
from utils.validation_util import ValidationUtils


class AttendanceController:
    
    @staticmethod
    async def get_all_attendances(
        name: str,
        date: str,
        checkin_status: StatusType,
        checkout_status: StatusType,
        paging: MsPagination,
    ) -> MsPaginationResult[AttendanceInDb]:
        query = {
            "isDelete": False
        }
        if name not in ["", None]:
            namePattern = re.compile(name, re.IGNORECASE)
            query["employeeDetail.name"] = {"$regex": namePattern}
        
        if date not in ["", None]:    
            try:
                if "/" in date:
                    date = date.split("/")
                elif ":" in date:
                    date = date[0:10].split("-")
                elif "-" in date:
                    date = date.split("-")
                else:
                    date = date.split(" ")

                date = datetime.strptime(
                    "-".join(date), "%m-%d-%Y"
                )
            except Exception as err:
                logger.error(err)
                raise HTTPException(
                    400, f"Format tanggal {date} tidak valid"
                )
            query["checkIn.timestamp"] = {"$gte": date, "$lte": date + timedelta(days=1)}
            
        if checkin_status not in ["", None]:
            query["checkIn.status"] = checkin_status
            
        if checkout_status not in ["", None]:
            query["checkOut.status"] = checkout_status
        
        return await Paginate(
            DB_ATTENDANCE,
            query,
            paging,
            None,
            AttendanceInDb
        )
    
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