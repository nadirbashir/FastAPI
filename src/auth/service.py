from uuid import UUID, uuid4
from sqlmodel import Session, select
from fastapi import Depends
from typing import Annotated
from . import models
from src.entities.user import User
from passlib.context import CryptContext
import jwt
from jwt import PyJWTError
from fastapi.security import APIKeyHeader
from datetime import datetime, timedelta, timezone
from ..exceptions import AuthenticationError    


#should be kept secret in .env and not hardcoded
SECRET_KEY = '197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_bearer = APIKeyHeader(name='Authorization')
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def register_user(db: Session, register_user_request: models.RegisterUserRequest) -> None:
    try:
        create_user_model = User(
            id=uuid4(),
            email=register_user_request.email,
            first_name=register_user_request.first_name,
            last_name=register_user_request.last_name,
            password_hash=get_password_hash(register_user_request.password)
        )    
        db.add(create_user_model)
        db.commit()
    except Exception as e:
        print(f"Failed to register user: {register_user_request.email}. Error: {str(e)}")
        raise
    
def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)

def create_access_token(email: str, user_id: UUID, expires_delta: timedelta) -> str:
     encode = {
        'sub': email,
        'id': str(user_id),
        'exp': datetime.now(timezone.utc) + expires_delta
    }
     return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
 
def authenticate_user(email: str, password: str, db: Session) -> User | bool:
    query = select(User).where(User.email == email)
    user = db.exec(query).first()
    if not user or not verify_password(password, user.password_hash):
        print(f"Failed authentication attempt for email: {email}")
        return False
    return user
 
def login_for_access_token(login_data: models.LoginRequest, db: Session) -> models.Token:
    user = authenticate_user(login_data.email, login_data.password, db)
    if not user:
        raise AuthenticationError()
    token = create_access_token(user.email, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return models.Token(access_token=token, token_type='bearer')


def verify_token(token: str) -> models.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get('id')
        return models.TokenData(user_id=user_id)
    except PyJWTError as e:
        print(f"Token verification failed: {str(e)}")
        raise AuthenticationError()

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> models.TokenData:
    if token.startswith('bearer '):
        token = token[len('bearer '):]
    return verify_token(token)

CurrentUser = Annotated[models.TokenData, Depends(get_current_user)]
