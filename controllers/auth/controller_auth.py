from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
import jwt
from pydantic import BaseModel, Field
from starlette import status

from config.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY
from helpers.user.user_util import UserUtils
from models.user.model_user import RoleType
from utils.datatypes_util import ObjectIdStr

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Sesi telah berakhir, silahkan login kembali!",
    headers={"WWW-Authenticate": "Bearer"},
)
ROLE_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User tidak memiliki akses",
    headers={"WWW-Authenticate": "Bearer"},
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class JwtToken(BaseModel):
    userId: ObjectIdStr = None
    name: str = None
    photoUrl: str = None
    email: str = None
    username: str = None
    role: str = None
    exp: int = None

class AuthController:

    def create_access_token(data: JwtToken, expires_delta: int):
        if expires_delta:
            expire = datetime.utcnow() + timedelta(minutes=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        data.exp = expire
        data.userId = str(data.userId)
        encoded_jwt = jwt.encode(data.model_dump(), JWT_SECRET_KEY, JWT_ALGORITHM)

        return encoded_jwt

    async def login_data(username: str, password: str):
        user = await UserUtils.get_user_by_username(username)
        if not user:
            raise HTTPException(404, "User not found")

        if password != user.password:
            raise HTTPException(401, "Username and password invalid")
        else:
            token_data = JwtToken.model_construct(user.model_fields_set, **user.model_dump())
            token_data.userId = user.id
            access_token = AuthController.create_access_token(token_data, ACCESS_TOKEN_EXPIRE_MINUTES)
            print("access_token done")
            token_data = token_data.model_dump()
            token_data["access_token"] = access_token
            return token_data


    def get_current_user_data(
            security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
    ):
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            data_token = JwtToken()
            data_token.userId = payload.get("userId")
            data_token.name = payload.get("name")
            data_token.username = payload.get("username")
            data_token.email = payload.get("email")
            data_token.exp = payload.get("exp")
            data_token.role = payload.get("role")
            data_token.photoUrl = payload.get("photoUrl")
            if str(security_scopes.scopes[0]).lower() == "*":
                print("Semua Role memiliki akses")
            elif RoleType[data_token.role] in security_scopes.scopes:
                print(f"Role {str(data_token.role).upper()} memiliki akases")
            elif RoleType[data_token.role] not in security_scopes.scopes:
                raise ROLE_EXCEPTION
        except jwt.PyJWTError:
            raise CREDENTIALS_EXCEPTION
        return data_token


    async def get_current_token_data(token: str = Depends(oauth2_scheme)):
        return token