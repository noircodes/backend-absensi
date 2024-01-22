import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette.responses import JSONResponse

from config.config import PROJECT_NAME
from controllers.user.controller_user import UserController
# from models.user.model_user import create_user_instances
from routers.auth.router_auth import router_auth
from routers.user.router_user import router_user
from routers.attendance.router_attendance_admin import router_attendance_admin
from routers.attendance.router_attendance import router_attendance


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting Backend-Personal-Cashflow")
    # check_user = await UserController.get_all_users()
    # if not check_user:
    #     await create_user_instances()
    #     logger.info("Initial User Created")
    #     print("initial user created")

    logging.info("*** Backend-Personal-Cashflow Started ***")
    yield


TITLE = "-".join(PROJECT_NAME.split(" "))

app = FastAPI(
    title=TITLE,
    lifespan=lifespan,
    swagger_ui_parameters={
        "tryItOutEnabled": False,
        "docExpansion": "none",
        "filter": True
    }
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    unprocessable_entity = HTTPStatus.UNPROCESSABLE_ENTITY
    return JSONResponse(
        status_code=unprocessable_entity.value,
        content=jsonable_encoder(
            {
                "detail": {
                    "status_code": str(unprocessable_entity.value),
                    "error": unprocessable_entity.phrase.upper(),
                    "type": "VALIDATION_ERROR",
                    "message": unprocessable_entity.phrase + ". " + str(exc),
                    "timestamp": datetime.now(timezone.utc)
                    .replace(microsecond=0)
                    .astimezone()
                    .isoformat(),
                    "method": request.method,
                    "path": request.url.path,
                    "query_params": request.query_params,
                    "location": exc.errors(),
                    "body": exc.body,
                }
            }
        ),
    )

@app.get("/")
async def root():
    return {"status": "ok"}

app.include_router(router_auth)
app.include_router(router_user)

app.include_router(router_attendance_admin)
app.include_router(router_attendance)

