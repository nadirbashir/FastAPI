from uuid import UUID
from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    
class PasswordChange(BaseModel):
    user_id: UUID
    current_password: str
    new_password: str
    confirm_password: str