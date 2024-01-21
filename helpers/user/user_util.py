from fastapi import HTTPException
from config.mongodb_collections import DB_USER
from models.user.model_user import UserInDb
from utils.validation_util import ValidationUtils


class UserUtils:
    
    @staticmethod
    async def get_user_by_id_or_404(user_id: str, devel_password: str = None):
        user = await DB_USER.find_one(
            {"isDelete": False, "_id": ValidationUtils.validate_objectid(user_id, "User ID")}
        )
        if not user:
            raise HTTPException(status_code=404, detail="User tidak ditemukan")
        result = UserInDb(**user)
        if devel_password:
            result.password = devel_password
        return result

    @staticmethod
    async def get_user_by_id(user_id: str, devel_password: str = None):
        user = await DB_USER.find_one(
            {"isDelete": False, "_id": ValidationUtils.validate_objectid(user_id, "User ID")}
        )
        if not user:
            return False
        result = UserInDb(**user)
        if devel_password:
            result.password = devel_password
        return result

    @staticmethod
    async def get_user_password_by_id_or_404(user_id: str):
        user = await DB_USER.find_one(
            {"isDelete": False, "_id": ValidationUtils.validate_objectid(user_id, "User ID")}
        )
        if not user:
            raise HTTPException(status_code=404, detail="User tidak ditemukan")
        result = UserInDb(**user)
        return result

    @staticmethod
    async def get_user_by_email(email: str):
        user = await DB_USER.find_one({"isDelete": False, "email": email})
        if user:
            return UserInDb(**user)
        return False

    @staticmethod
    async def get_user_by_email_and_username(email: str, username: str):
        user = await DB_USER.find_one(
            {"isDelete": False, "email": email, "username": username}
        )
        if user:
            return UserInDb(**user)
        return False

    @staticmethod
    async def get_user_by_phone(phone: str):
        user = await DB_USER.find_one({"isDelete": False, "phone": phone})
        if user:
            return UserInDb(**user)
        return False

    @staticmethod
    async def get_user_by_username(username: str):
        user = await DB_USER.find_one({"isDelete": False, "username": username})
        print(user)
        if user:
            return UserInDb(**user)
        return False

    @staticmethod
    async def get_user_by_account_id(account_id: str):
        user = await DB_USER.find_one(
            {
                "isDelete": False,
                "account_id": ValidationUtils.validate_objectid(account_id, "Account ID"),
            }
        )
        if user:
            return UserInDb(**user)
        return False