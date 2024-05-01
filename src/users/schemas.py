import datetime
import uuid
from uuid import UUID

from users.models import EnvStatus, TypeUser
from pydantic import BaseModel, ConfigDict, EmailStr


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


# class Users(ShowUser):
#     model_config = ConfigDict(from_attributes=True)


# class Product(ProductBase):
#     model_config = ConfigDict(from_attributes=True)

#     id: int