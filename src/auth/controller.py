from fastapi import APIRouter, Request
from starlette import status
from . import  models
from . import service
# from fastapi.security import OAuth2PasswordRequestForm
from src.database.core import DbSession
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(request: Request, db: DbSession,
                      register_user_request: models.RegisterUserRequest):
    print(f"Registering user: {register_user_request.email}")
    service.register_user(db, register_user_request)


@router.post("/login", response_model=models.Token)
async def login_for_access_token(login_data: models.LoginRequest, db: DbSession):
    return service.login_for_access_token(login_data, db)


