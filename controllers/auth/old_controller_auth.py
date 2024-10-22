from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from starlette import status
import datetime as _datetime
from typing import Annotated

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
    userId: ObjectIdStr | str
    name: str | None = None
    photoUrl: str | None = None
    email: str | None = None
    username: str | None = None
    role: str
    exp: int | None = None

class AuthController:
    @staticmethod
    def create_access_token(data: JwtToken, expires_delta: int):
        if expires_delta:
            expire = datetime.now(_datetime.timezone.utc) + timedelta(minutes=expires_delta)
        else:
            expire = datetime.now(_datetime.timezone.utc) + timedelta(minutes=15)
        data.exp = int(expire.timestamp())
        data_to_encode = data.model_dump()
        data_to_encode["userId"] = str(data_to_encode["userId"])
        encoded_jwt: str = jwt.encode(data_to_encode, JWT_SECRET_KEY, JWT_ALGORITHM) # type: ignore

        return encoded_jwt

    @staticmethod
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

    @staticmethod
    def get_current_user_data(
            security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
    ):
        print("test")
        try:
            print('flag 1')
            print(token)    
            payload = jwt.decode(
                token,
                JWT_SECRET_KEY,
                algorithms=[JWT_ALGORITHM],
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "require_exp": True
                }) # type: ignore
            print('flag 2')
            data_token = JwtToken(userId=payload.get("userId"), role=payload.get("role"))
            data_token.name = payload.get("name")
            data_token.username = payload.get("username")
            data_token.email = payload.get("email")
            data_token.exp = payload.get("exp")
            if not data_token.exp or datetime.fromtimestamp(data_token.exp, _datetime.timezone.utc) < datetime.now(_datetime.timezone.utc):
                raise CREDENTIALS_EXCEPTION
            data_token.photoUrl = payload.get("photoUrl")
            if str(security_scopes.scopes[0]).lower() == "*":
                print("Semua Role memiliki akses")
            elif RoleType[data_token.role] in security_scopes.scopes:
                print(f"Role {str(data_token.role).upper()} memiliki akases")
            elif RoleType[data_token.role] not in security_scopes.scopes:
                raise ROLE_EXCEPTION
        except InvalidTokenError:
            raise CREDENTIALS_EXCEPTION
        return data_token

    @staticmethod
    async def get_current_token_data(token: str = Depends(oauth2_scheme)):
        return token