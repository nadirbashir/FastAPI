from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, Session

DATABASE_URL: str = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)

def get_db():
    with Session(engine) as db:
            yield db # db.close() is called automatically after yield
            
DbSession = Annotated[Session, Depends(get_db)]