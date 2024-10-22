from fastapi import APIRouter, Depends, Security
from controllers.attendance.controller_attendance import AttendanceController
from controllers.auth.controller_auth import AuthController, JwtToken
from models.attendance.model_attendance import AttendanceInDb, StatusType
from utils.datatypes_util import ObjectIdStr
from utils.pagination.model_pagination_util import MsPagination, MsPaginationResult


router_attendance_admin = APIRouter(prefix="/admin/attendance", tags=["Attendance Service - ADMIN"])

@router_attendance_admin.get("", response_model=MsPaginationResult[AttendanceInDb])
async def admin_get_all_attendances(
    name: str | None = None,
    date: str | None = None,
    employee_id: ObjectIdStr | None = None,
    checkin_status: StatusType | None = None,
    checkout_status: StatusType | None = None,
    paging: MsPagination = Depends(MsPagination.QueryParam),
    credential: JwtToken = Security(
        AuthController.get_current_user_data,
        scopes=["ADMIN"]
    )
):
    return await AttendanceController.get_all_attendances(
        name,
        date,
        employee_id,
        checkin_status,
        checkout_status,
        paging
    )

@router_attendance_admin.get("/{id}", response_model=AttendanceInDb)
async def admin_get_attendance_by_id(
    id: ObjectIdStr,
    credential: JwtToken = Security(
        AuthController.get_current_user_data,
        scopes=["ADMIN"]
    )
):
    return await AttendanceController.get_attendance_by_id(id)

@router_attendance_admin.post("/tap/{attendanceMethod}", response_model=AttendanceInDb)
async def admin_tap_attendance(
    attendanceMethod: str,
    credential: JwtToken = Security(
        AuthController.get_current_user_data,
        scopes=["ADMIN"]
    )
):
    return await AttendanceController.tap_attendance(attendanceMethod, credential.userId)

@router_attendance_admin.delete("/{id}")
async def admin_delete_attendance(
    id: ObjectIdStr,
    credential: JwtToken = Security(
        AuthController.get_current_user_data,
        scopes=["ADMIN"]
    )
):
    return await AttendanceController.delete_attendance(id, credential.userId)