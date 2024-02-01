from typing import List
from fastapi import APIRouter, Depends, Security
from controllers.attendance.controller_attendance import AttendanceController
from controllers.auth.controller_auth import AuthController, JwtToken
from models.attendance.model_attendance import Attendance, AttendanceInDb, StatusType
from utils.datatypes_util import ObjectIdStr
from utils.pagination.model_pagination_util import MsPagination


router_attendance = APIRouter(prefix="/attendance", tags=["Attendance Service - EMPLOYEE"])

@router_attendance.get("", response_model=List[AttendanceInDb])
async def employee_get_all_attendances(
    name: str = None,
    date: str = None,   
    checkin_status: StatusType = None,
    checkout_status: StatusType = None,
    paging: MsPagination = Depends(MsPagination.QueryParam),
    credential: JwtToken = Security(
        AuthController.get_current_user_data,
        scopes=["EMPLOYEE"]
    )
):
    return await AttendanceController.get_all_attendances(
        name,
        date,
        checkin_status,
        checkout_status,
        paging
    )

@router_attendance.get("/{id}", response_model=AttendanceInDb)
async def employee_get_attendance_by_id(
    id: ObjectIdStr,
    credential: JwtToken = Security(
        AuthController.get_current_user_data,
        scopes=["EMPLOYEE"]
    )
):
    return await AttendanceController.get_attendance_by_id(id)

@router_attendance.post("/tap/{attendanceMethod}", response_model=AttendanceInDb)
async def employee_create_attendance(
    attendanceMethod: str,
    credential: JwtToken = Security(
        AuthController.get_current_user_data,
        scopes=["EMPLOYEE"]
    )
):
    return await AttendanceController.tap_attendance(attendanceMethod, credential.userId)


@router_attendance.delete("/{id}")
async def employee_delete_attendance(
    id: ObjectIdStr,
    credential: JwtToken = Security(
        AuthController.get_current_user_data,
        scopes=["EMPLOYEE"]
    )
):
    return await AttendanceController.delete_attendance(id, credential.userId)