from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

from config.config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from helpers.user.user_util import UserUtils
from utils.datatypes_util import ObjectIdStr
from models.user.model_user import RoleType



class JwtToken(BaseModel):
    userId: ObjectIdStr
    name: str | None = None
    photoUrl: str | None = None
    email: str | None = None
    username: str | None = None
    role: str
    exp: int | None = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

app = FastAPI()

class AuthController:
    @staticmethod
    async def login_data(username: str, password: str):
        user = await UserUtils.get_user_by_username( username)
        if not user:
            raise HTTPException(404, "User tidak ditemukan")
        if password != user.password:
            raise HTTPException(401, "Password anda salah")
        token_data = JwtToken.model_construct(user.model_fields_set, **user.model_dump())
        token_data.userId = user.id
        access_token = AuthController.create_access_token(token_data, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)
        c_token_data = token_data.model_dump()
        c_token_data["access_token"] = access_token
        return c_token_data

    @staticmethod
    def create_access_token(data: JwtToken, expires_delta: int | None = None):
        to_encode = data.model_dump()
        if expires_delta:
            expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        to_encode.update({"userId": str(data.userId)})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM) # type: ignore
        return encoded_jwt

    @staticmethod
    def get_current_user_data(token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]) # type: ignore
            userId = payload.get("userId")
            name = payload.get("name")
            photoUrl = payload.get("photoUrl")
            email = payload.get("email")
            username = payload.get("username")
            role = payload.get("role")
            exp = payload.get("exp")
            data_token = JwtToken(
                userId=userId,
                name=name,
                photoUrl=photoUrl,
                email=email,
                username=username,
                role=role,
                exp=exp
            )
        except InvalidTokenError:
            raise credentials_exception
        print(data_token)
        return data_token
    
    @staticmethod
    def auth_role_admin(current_user: Annotated[JwtToken, Depends(get_current_user_data)]):
        print(current_user)
        if current_user.role != RoleType.ADMIN:
            raise HTTPException(403, "User tidak memiliki hak akses")
        return current_user

    @staticmethod
    def auth_role_employee(current_user: Annotated[JwtToken, Depends(get_current_user_data)]):
        if current_user.role != RoleType.EMPLOYEE:
            raise HTTPException(403, "User tidak memiliki hak akses")
        return current_user
