from typing import List
from fastapi import HTTPException
from loguru import logger
from helpers.user.user_util import UserUtils
from models.user.model_user import UserInDb, UserRequest, UserUpdate, UserView
from utils.datatypes_util import ObjectIdStr
from utils.datetimes_util import DatetimeUtils
from utils.validation_util import ValidationUtils
from config.mongodb_collections import DB_USER
from pymongo.results import InsertOneResult, UpdateResult



class UserHelper:
    
    @staticmethod
    async def get_all_users() -> List[UserInDb]:
        query = {
            "isDelete": False
        }
        try:
            result = await DB_USER.find(query).to_list(None)
            return result
        except Exception as err:
            logger.error(err)
            raise HTTPException(500, "Gagal menampilkan data user")
        
    @staticmethod
    async def get_user_by_id(
        id: ObjectIdStr
    ) -> UserInDb:
        query = {
            "isDelete": False,
            "_id": id
        }
        try:
            result = await DB_USER.find_one(query)
            if not result:
                raise HTTPException(404, "User tidak ditemukan")
            return UserInDb(**result)
        except Exception as err:
            logger.error(err)
            raise HTTPException(500, "Gagal menampilkan data user")
    
    @staticmethod
    async def create_user(
        request: UserRequest,
        user_id: ObjectIdStr
    ) -> UserInDb:
        user_base = UserView(**request.model_dump())
        user_base.createTime = DatetimeUtils.datetime_now()
        user_base.createdBy = user_id
        user_base.isDelete = False
        
        try:
            op_create_user: InsertOneResult = await DB_USER.insert_one(user_base.model_dump())
        except Exception as err:
            logger.error(err)
            op_create_user = None
            raise HTTPException(500, "Gagal menambahkan user")
        
        return await UserUtils.get_user_by_id_or_404(op_create_user.inserted_id)
    
    @staticmethod
    async def update_user(
        id: ObjectIdStr,
        request: UserUpdate,
        user_id: ObjectIdStr
    ) -> UserInDb:
        user_update = request.model_dump()
        user_update["updateTime"] = DatetimeUtils.datetime_now()
        user_update["updatedBy"] = user_id
        
        try:
            op_update_user: UpdateResult = await DB_USER.update_one(
                {"_id": id},
                {"$set": user_update}
            )
            return await UserUtils.get_user_by_id_or_404(id)
        except Exception as err:
            logger.error(err)
            raise HTTPException(500, "Gagal mengubah data user")
        
    @staticmethod
    async def delete_user(
        id: ObjectIdStr,
        user_id: ObjectIdStr
    ):
        try:
            delete_user: UpdateResult = await DB_USER.update_one(
                {"_id": id},
                {
                    "$set": {
                        "deleteTime": DatetimeUtils.datetime_now(),
                        "deleteBy": user_id,
                        "isDelete": True
                    }
                }
            )
            return {"detail": "Data user berhasil terhapus"}
        except Exception as err:
            logger.error(err)
            raise HTTPException(500, "Gagal menghapus data user")