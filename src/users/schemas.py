import uuid

from src.users.models import EnvStatus, TypeUser
from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    login: EmailStr
    password: str
    project_id: uuid.UUID
    env: EnvStatus
    domain: TypeUser


class ShowUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    login: EmailStr
    project_id: uuid.UUID
    env: EnvStatus
    domain: TypeUser
