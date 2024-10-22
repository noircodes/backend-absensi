import re
from typing import Any, List

from fastapi import HTTPException
from config.mongodb_collections import DB_USER
from helpers.user.helper_user import UserHelper
from models.user.model_user import UserInDb, UserRequest, UserResponse, UserUpdate
from utils.datatypes_util import ObjectIdStr
from utils.pagination.model_pagination_util import MsPagination, MsPaginationResult
from utils.pagination.pagination_util import Paginate
from utils.validation_util import ValidationUtils


class UserController:
    
    @staticmethod
    async def get_all_users(
        name: str | None,
        role: str | None
    ) -> List [UserResponse]:
        datas =  await UserHelper.get_all_users(
            name,
            role,
            UserResponse
        )

        return datas
    
    @staticmethod
    async def get_users_in_pagination(
        name: str | None,
        role: str | None,
        paging: MsPagination
    ) -> MsPaginationResult[UserResponse]:
        query: dict[str, Any] = {
            "isDelete": False
        }
        if name is not None:
            if len(name.strip()) != 0:
                namePattern = re.compile(name, re.IGNORECASE)
                query["name"] = {"$regex": namePattern}
            
        if role is not None:
            query["role"] = role
        
        return await Paginate(
            DB_USER,
            query,
            paging,
            UserResponse,
            None
        )
    
    @staticmethod
    async def get_user_by_id(
        id: ObjectIdStr
    ) -> UserInDb:
        return await UserHelper.get_user_by_id(id)
    
    @staticmethod
    async def create_user(
        request: UserRequest,
        user_id: ObjectIdStr
    ) -> UserInDb:
        if user_id:
            user_id = ValidationUtils.validate_objectid(user_id, "UserId") # type: ignore
        
        if request.username in ["", None]:
            raise HTTPException(400, "Username tidak boleh kosong")
        
        if request.password in ["", None]:
            raise HTTPException(400, "Password tidak boleh kosong")
        
        if request.email is not None:
            ValidationUtils.validate_email(request.email)
            
        if request.phone is not None:
            ValidationUtils.validate_phone(request.phone)
        return await UserHelper.create_user(request, user_id)
    
    @staticmethod
    async def update_user(
        id: ObjectIdStr,
        request: UserUpdate,
        user_id: ObjectIdStr
    ) -> UserInDb | None:
        current_data = await UserHelper.get_user_by_id(id)
        if not current_data:
            raise HTTPException(404, "User tidak ditemukan")
        
        if request.email is not None:
            ValidationUtils.validate_email(request.email)
            
        if request.phone is not None:
            ValidationUtils.validate_phone(request.phone)
        
        return await UserHelper.update_user(id, request, user_id)
    
    @staticmethod
    async def delete_user(
        id: ObjectIdStr,
        user_id: ObjectIdStr
    ) -> dict[str, Any]:
        return await UserHelper.delete_user(id, user_id)