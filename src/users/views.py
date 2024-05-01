from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


from users.crud import create_user
from users.crud import get_users
from users.models import EnvStatus, TypeUser
from users.schemas import UserCreate, ShowUser
from uuid import UUID
from db import get_db

user_router = APIRouter(tags=['User'])


@user_router.post('/', response_model=UserCreate)
async def create_new_user(
        login: str,
        password: str,
        project_id: UUID,
        env: EnvStatus,
        domain: TypeUser,
        db: AsyncSession = Depends(get_db)
):
    new_user = await create_user(
        db=db,
        login=login,
        password=password,
        project_id=project_id,
        env=env,
        domain=domain
        )
    
    return new_user    


@user_router.get('/users', response_model=list[ShowUser])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    users = await get_users(db=db)
    return users
