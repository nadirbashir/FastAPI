from uuid import UUID
from sqlmodel import Session, select
from . import models
from src.entities.user import User
from src.exceptions import UserNotFoundError, InvalidPasswordError, PasswordMismatchError
from ..auth.service import verify_password, get_password_hash


def get_user_by_id(db: Session, user_id: UUID) -> models.UserResponse:
    query = select(User).where(User.id == user_id)
    user = db.exec(query).first()
    if not user:
        raise UserNotFoundError(user_id)
    print(f"Successfully retrieved user with ID: {user_id}")
    return user


def change_password(db: Session, user_id: UUID, password_change: models.PasswordChange) -> None:
    try:
        user = get_user_by_id(db, user_id)
        
        if not user:
            raise UserNotFoundError()
        # Verify current password
        if not verify_password(password_change.current_password, user.password_hash):
            print(f"Invalid current password")
            raise InvalidPasswordError()
        
        # Verify new passwords match
        if password_change.new_password != password_change.confirm_password:
            print(f"Password mismatch")
            raise PasswordMismatchError()
        
        # Update password
        user.password_hash = get_password_hash(password_change.new_password)
        db.commit()
        print(f"Password successfully changed")
    except Exception as e:
        print(f"Error during password change for user ID: {user_id}. Error: {str(e)}")
        raise
