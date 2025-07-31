from sqlmodel import SQLModel, Field
import uuid
from typing import Optional
from uuid import UUID

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    email: str = Field(unique=True, nullable=False, index=True)
    first_name: str = Field(nullable=False)
    last_name: Optional[str] = Field(default=None, nullable=True)
    password_hash: str = Field(nullable=False)
    
    
    def __repr__(self):
            return f"<User(email='{self.email}', first_name='{self.first_name}', last_name='{self.last_name}')>" 