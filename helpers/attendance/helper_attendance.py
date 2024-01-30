from datetime import date, datetime, timedelta
import re
from typing import List, Union
from fastapi import HTTPException
from loguru import logger
from helpers.attendance.attendance_util import AttendanceUtils
from helpers.user.helper_user import UserHelper
from models.attendance.model_attendance import Attendance, AttendanceInDb, AttendanceView, StatusType
from utils.datatypes_util import ObjectIdStr
from utils.datetimes_util import DatetimeUtils
from config.mongodb_collections import DB_ATTENDANCE
from pymongo.results import InsertOneResult, UpdateResult


class AttendanceHelper:
    
    @staticmethod
    async def get_all_attendances(
        name: str,
        date: str,
        checkin_status: StatusType,
        checkout_status: StatusType
    ) -> List[AttendanceInDb]:
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
                    "-".join(date), "%d-%m-%Y"
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
            
        try:
            result = await DB_ATTENDANCE.find(query).to_list(None)
            return result
        except Exception as err:
            logger.error(err)
            raise HTTPException(500, "Gagal menampilkan data absensi")
        
    @staticmethod
    async def get_attendance_by_id(
        id: ObjectIdStr
    ) -> AttendanceInDb:
        query = {
            "isDelete": False,
            "_id": id
        }
        try:
            result = await DB_ATTENDANCE.find_one(query)
            if not result:
                raise HTTPException(404, "Absensi tidak ditemukan")
            return result
        except Exception as err:
            logger.error(err)
            raise HTTPException(500, "Gagal menampilkan data absensi")
        
    @staticmethod
    async def get_attendance_by_employee_id_and_today(
        employee_id: ObjectIdStr,
        is_already_check_out: bool = False
    ) -> Union[AttendanceInDb, bool]:
        query = {
            "isDelete": False,
            "employeeDetail.employeeId": employee_id
        }
        if is_already_check_out:
            query["checkOut.timestamp"] = {"$ne" : None}
        
        datetime_now = DatetimeUtils.date_now()
        today_start = datetime(datetime_now.year, datetime_now.month, datetime_now.day, 0, 0, 0)
        today_end = today_start + timedelta(1)
        query["createTime"] = {
            "$gt": today_start,
            "$lt": today_end
        }
        result = await DB_ATTENDANCE.find_one(query)
        if not result:
            return False
        return AttendanceInDb(**result)
    
    @staticmethod
    async def create_attendance(
        request: Attendance,
        user_id: ObjectIdStr
    ) -> AttendanceInDb:
        attendance_base = AttendanceView(**request.model_dump())
        
        # Lookup user data, then insert to employee detail
        user_data = await UserHelper.get_user_by_id(user_id)
        attendance_base.employeeDetail.employeeId = user_id
        attendance_base.employeeDetail.name = user_data.name
        attendance_base.employeeDetail.noId = user_data.noId
        attendance_base.employeeDetail.photoUrl = user_data.photoUrl
        
        attendance_base.createTime = DatetimeUtils.datetime_now()
        attendance_base.createdBy = user_id
        attendance_base.isDelete = False
        
        try:
            op_create_user: InsertOneResult = await DB_ATTENDANCE.insert_one(attendance_base.model_dump())
        except Exception as err:
            logger.error(err)
            op_create_user = None
            raise HTTPException(500, "Gagal menambahkan data absensi")
        
        return await AttendanceUtils.get_attendance_by_id_or_404(op_create_user.inserted_id)
    
    @staticmethod
    async def update_attendance(
        id: ObjectIdStr,
        request: Attendance,
        user_id: ObjectIdStr
    ) -> AttendanceInDb:
        attendance_update = request.model_dump(exclude_unset=True)
        attendance_update["updateTime"] = DatetimeUtils.datetime_now()
        attendance_update["updatedBy"] = user_id
        
        try:
            op_update_attendance: UpdateResult = await DB_ATTENDANCE.update_one(
                {"_id": id},
                {"$set": attendance_update}
            )
            return await AttendanceUtils.get_attendance_by_id_or_404(id)
        except Exception as err:
            logger.error(err)
            raise HTTPException(500, "Gagal mengubah data absensi")
        
    @staticmethod
    async def delete_attendance(
        id: ObjectIdStr,
        user_id: ObjectIdStr
    ):
        try:
            delete_attendance: UpdateResult = await DB_ATTENDANCE.update_one(
                {"_id": id},
                {
                    "$set": {
                        "deleteTime": DatetimeUtils.datetime_now(),
                        "deleteBy": user_id,
                        "isDelete": True
                    }
                }
            )
            return {"detail": "Data absensi berhasil terhapus"}
        except Exception as err:
            logger.error(err)
            raise HTTPException(500, "Gagal menghapus data absensi")