import re
from typing import Any, List
from fastapi import HTTPException
from loguru import logger
from helpers.user.user_util import UserUtils
from models.user.model_user import UserInDb, UserRequest, UserUpdate, UserView
from utils.datatypes_util import ObjectIdStr
from utils.datetimes_util import DatetimeUtils
from config.mongodb_collections import DB_USER
from pymongo.results import InsertOneResult, UpdateResult
from utils.datatypes_util import TGenericBaseModel

class UserHelper:
    
    @staticmethod
    async def get_all_users(
        name: str | None,
        role: str | None,
        resultClass: type[TGenericBaseModel] = UserView
    ) -> List[TGenericBaseModel]:
        query: dict[str, Any] = {
            "isDelete": False
        }
        if name is not None:
            if len(name.strip()) != 0:
                namePattern = re.compile(name, re.IGNORECASE)
                query["name"] = {"$regex" : namePattern}
            
        if role not in ["", None]:
            query["role"] = role
            
        try:
            cursor = DB_USER.find(
                query,
                resultClass.Projection(),
            )
            results: list[dict[str, Any]] = await cursor.to_list(None) # type: ignore
            return [resultClass(**result) for result in results]
        except Exception as err:
            logger.error(err)
            raise HTTPException(500, "Gagal menampilkan data user")
        
    @staticmethod
    async def get_user_by_id(
        id: ObjectIdStr
    ) -> UserInDb:
        query: dict[str, Any] = {
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
            raise HTTPException(500, "Gagal menambahkan user")
        
        return await UserUtils.get_user_by_id_or_404(op_create_user.inserted_id)
    
    @staticmethod
    async def update_user(
        id: ObjectIdStr,
        request: UserUpdate,
        user_id: ObjectIdStr
    ) -> UserInDb | None:
        user_update = request.model_dump()
        user_update["updateTime"] = DatetimeUtils.datetime_now()
        user_update["updatedBy"] = user_id
        
        try:
            op_update_user: UpdateResult = await DB_USER.update_one(
                {"_id": id},
                {"$set": user_update}
            )
            if op_update_user.matched_count > 0:
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
            await DB_USER.update_one(
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