from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from controllers.auth.controller_auth import AuthController


router_auth = APIRouter(prefix="/auth", tags=["Authentication Service"])

@router_auth.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    return await AuthController.login_data(username, password)