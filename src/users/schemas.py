import uuid

from src.users.models import EnvStatus, TypeUser
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    login: EmailStr
    password: str
    project_id: uuid.UUID
    env: EnvStatus
    domain: TypeUser

    class Config:
        from_attributes = True


class ShowUser(BaseModel):
    id: uuid.UUID
    login: EmailStr
    project_id: uuid.UUID
    env: EnvStatus
    domain: TypeUser

    class Config:
        from_attributes = True
