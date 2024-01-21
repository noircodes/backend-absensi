from typing import List
from fastapi import APIRouter, Security
from controllers.auth.controller_auth import AuthController, JwtToken
from controllers.user.controller_user import UserController
from models.user.model_user import UserInDb, UserRequest, UserUpdate
from utils.datatypes_util import ObjectIdStr


router_user = APIRouter(prefix="/user", tags=["User Service"])

@router_user.get("", response_model=List[UserInDb])
async def get_all_users(
    credential: JwtToken = Security(
        AuthController.get_current_user_data,
        scopes=["*"]
    )
):
    return await UserController.get_all_users()

@router_user.get("/{id}", response_model=UserInDb)
async def get_user_by_id(
    id: ObjectIdStr,
    credential: JwtToken = Security(
        AuthController.get_current_user_data,
        scopes=["*"]
    )
):
    return await UserController.get_user_by_id(id)

@router_user.post("", response_model=UserInDb)
async def create_user(
    request: UserRequest,
    credential: JwtToken = Security(
        AuthController.get_current_user_data,
        scopes=["*"]
    )
):
    return await UserController.create_user(request, credential.userId)

@router_user.put("/{id}", response_model=UserInDb)
async def update_user(
    id: ObjectIdStr,
    request: UserUpdate,
    credential: JwtToken = Security(
        AuthController.get_current_user_data,
        scopes=["*"]
    )
):
    return await UserController.update_user(id, request, credential.userId)

@router_user.delete("/{id}")
async def delete_user(
    id: ObjectIdStr,
    credential: JwtToken = Security(
        AuthController.get_current_user_data,
        scopes=["*"]
    )
):
    return await UserController.delete_user(id, credential.userId)