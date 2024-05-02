from fastapi import APIRouter, HTTPException
from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession


from src.users.crud import create_user
from src.users.crud import get_users
from src.users.crud import get_user_by_id
from src.users.crud import put_locktime
from src.users.crud import reset_locktime
from src.users.models import EnvStatus, TypeUser, User
from src.users.schemas import UserCreate, ShowUser
from uuid import UUID
from src.db import get_db

user_router = APIRouter(tags=['User'])


@user_router.post('/', response_model=UserCreate)
async def create_new_user(
        login: EmailStr,
        password: str,
        project_id: UUID,
        env: EnvStatus,
        domain: TypeUser,
        db: AsyncSession = Depends(get_db)
) -> User:
    new_user = await create_user(
        db=db,
        login=login,
        password=password,
        project_id=project_id,
        env=env,
        domain=domain
    )
    return new_user


@user_router.get('/all_users', response_model=list[ShowUser])
async def get_all_users(db: AsyncSession = Depends(get_db)) -> list[ShowUser]:
    users = await get_users(db=db)
    return users


@user_router.post('/acquire', response_model=ShowUser)
async def acquire_lock(user_id: UUID, db: AsyncSession = Depends(get_db)) -> ShowUser:
    current_user = await get_user_by_id(user_id=user_id, db=db)
    if not current_user:
        raise HTTPException(status_code=404, detail=("User doesn't exists"))

    if current_user.locktime:
        raise HTTPException(status_code=423, detail=("User has already been issued"))

    locked_user = await put_locktime(user=current_user, db=db)
    return locked_user


@user_router.post('/release', response_model=ShowUser)
async def release_lock(user_id: UUID, db: AsyncSession = Depends(get_db)) -> ShowUser:
    current_user = await get_user_by_id(user_id=user_id, db=db)
    if not current_user:
        raise HTTPException(status_code=404, detail=("User dosen't exists"))
    released_user = await reset_locktime(user=current_user, db=db)
    return released_user
